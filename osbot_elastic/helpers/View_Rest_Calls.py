
####### use this to see REST calls made to the Elastic endpoint #######
# good to debug performance issues

from os import environ
from pprint import pprint

from elasticsearch.transport import Transport
from osbot_utils.testing.Hook_Method import Hook_Method

class View_Rest_Calls:

    def __init__(self):
        self.target_module  = Transport
        self.target_method  = "perform_request"
        self.wrap_method    = None
        self.calls          = []

    def __enter__(self):
        return self.start()

    def __exit__(self, type, value, traceback):
        self.stop()

    def after_call(self, return_value, args, kwargs):
        call = {
                    'method'      : args[1]               ,
                    'url'         : args[2]               ,
                    'headers'     : kwargs.get('headers') ,
                    'params'      : kwargs.get('params' ) ,
                    'body'        : kwargs.get('body'   ) ,
                    'return_value': return_value
                }
        self.calls.append(call)
        return return_value

    def print_calls_made(self, print_calls=True, print_return_value=False):
        print()
        print("#######################################################")
        print("##### REST calls made to Elastic Server           #####")
        print("#######################################################")
        print()
        if print_calls:
            print(f"{'Method':<8} {'Url':<20} {'Params':<10}")
        for call in self.calls:
            if print_calls:
                print(f"{call['method']:<8} {call['url']:<20} {str(call['params']):<10}")
            if print_return_value:
                print(call['return_value'])
                print()

    def start(self):
        self.wrap_target_method()
        return self

    def stop(self):
        self.unwrap_target_method()
        return self

    def wrap_target_method(self):
        self.wrap_method = Hook_Method(self.target_module, self.target_method)
        self.wrap_method.add_on_after_call(self.after_call)
        self.wrap_method.wrap()

    def unwrap_target_method(self):
        self.wrap_method.unwrap()