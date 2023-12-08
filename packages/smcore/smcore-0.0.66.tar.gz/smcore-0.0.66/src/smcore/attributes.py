import re
import asyncio
from .enums import PromiseState
from .types_pb2 import Promise

import pycurl

def parse_promise(promise_string: str):
    result = re.search("Promise\(\s*([-*\w]+)\s+as\s+([-*\w]+)\s+from\s+([-*\w]+)\s*\)", promise_string)
    if result == None:
        result = re.search("^Promise", promise_string)
        if result != None:
            raise Exception(f"possible Promise detected '{promise_string}'; please check name, type, and source for spelling")
        else:
            return None
        
    p = Promise(name=result.group(1),
                type=result.group(2),
                source=result.group(3),
                state=PromiseState.PENDING,
                data=None)

    return p

class _SafePromise():
    promise = None
    fulfilled = asyncio.Event()

    def __init__(self, promise):
        self.promise = promise
    
class Attributes():
    c = pycurl.Curl()
    attributes = {}
    promises = {}
    
    # attrs here is a raw attributes dictionary returned from
    # default_args.
    def __init__(self, attrs):

        # Split into attributes and promises
        for attr_name, attr_val in attrs.items():
            
            # Check first if promise
            try:
                p = parse_promise(attr_val)
                self.promises[attr_name] = SafePromise(p)
                continue
            except:
                pass

            self.attributes[attr_name] = attr_val
    
    # def __getitem__(self, item): pass
        
    # Read attribute value successfully (promises resolved) or throw exception
    # (behavior is matched accross Go and python)
    def value(self, key):

        # Handle promise case first
        try:
            p = self.promises[key]

            if (p.state == PromiseState.FULFILLED or
                p.state == PromiseState.FINAL):
                
                # (NOTE: This should probably be done when the result
                # arrives to minimize agent idle time. That being said, I kind of
                # want to try it here and see if people complain. This will minimize
                # server-side load by not oversharing until agents are *ready* to use
                # the data. We'll switch if we need to.)
                content_type = p.WhichOneof("contents")
                if content_type == "data":
                    return p.data
                elif content_type == "link":
                    #resp = requests.get(p.link, allow_redirects=True)
                    #resp.raise_for_status() # Throw exception if anything went wrong

                    buff = io.BytesIO()
                    self.c.setopt(self.c.URL, p.link)
                    self.c.setopt(self.c.WRITEDATA, buff)
                    self.c.perform()
                    self.c.reset()
                    
                    return buff.getvalue()
                else:
                    return ("unrecognized content type: " + content_type).encode(encoding="utf-8")

                return p.data
            else:
                raise Exception(f"attempted to get value of unfulfilled promise")
            
        except KeyError:
            pass
        except Exception as e:
            raise e

        # If it wasn't a promise we return the value. This will raise a key error
        # if the value requested by the user doesn't exist
        return self.attributes[key]

    # This function behaves the same as "value", however it is
    # designed to be awaited when the value is a promise.  Otherwise, functions
    # the same as the value method
    async def await_value(self, key):

        # Check if promise first, await if no error thrown
        try:
            prom = self.promises[key]
            await self.promises[key].fulfilled
            return self.promises[key].data
        except KeyError:
            pass
        except Exception as e:
            raise e
        
        # If it wasn't a promise we return the value. This will raise a key error
        # if the value requested by the user doesn't exist
        return self.attributes[key]

    def _contains(self, promise):

        # "promise" is the incoming promise we're checking
        # "curr_prom" is one of our promised attributes we've already parsed
        for name, curr_prom in self.promises.items():
            data_id_match = (promise.name == curr_prom.name) or (curr_prom.name == "*")
            data_type_match = (promise.type == curr_prom.type) or (curr_prom.type == "*")
            source_match = (promise.source == curr_prom.source) or (curr_prom.source == "*")

            if data_type_match and data_id_match and source_match:
                return (name, True)

        return None, False
            
    def _fulfill(self, key, prom):
        self.promises[key] = SafePromise(prom)
        self.promises[key].fulfilled.set()
        #self.fulfillment_tracker[key].set()
        
    def all_fulfilled(self):
        for key, prom in self.promises.items():
            if prom.state == PromiseState.PENDING:
                return False
            
        return True