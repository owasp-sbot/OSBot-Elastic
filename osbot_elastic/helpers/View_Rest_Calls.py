
####### use this to see REST calls made to the Elastic endpoint #######
# good to debug performance issues

from os import environ
from pprint import pprint

from elasticsearch.transport import Transport
from osbot_utils.testing.Hook_Method import Hook_Method

class View_Rest_Calls:

    def __init__(self, show_xml=False, show_calls=True):
        self.show_xml       = show_xml
        self.show_calls     = show_calls
        self.target_module  = Transport
        self.target_method  = "perform_request"
        self.wrap_method    = None
        self.calls          = []

    def __enter__(self):
        return self.start()

    def __exit__(self, type, value, traceback):
        self.stop()

    def after_call(self, return_value):
        print('--- after call---')
        pprint(return_value)
        return return_value

    def before_call(self, *args, **kwargs):
        call = {
                    'method' : args[1],
                    'url'    : args[2],
                    'headers': kwargs.get('headers'),
                    'params' : kwargs.get('params' ),
                    'body'   : kwargs.get('body'   )

                }
        #pprint(call)
        # print('---- args ---- ')
        # pprint(args)
        # print('---- kwargs ---- ')
        # pprint(kwargs)
        return (args, kwargs)

    def start(self):
        self.wrap_target_method()
        if self.show_calls or self.show_xml:
            print()
            print("*******************************************************")
            print("***** Starting showing REST calls to elastic endpoint *****")
            print("*******************************************************")
        if self.show_calls:
            environ['show_rest_calls'    ] = "True"
        if self.show_xml:
            environ['show_rest_calls_xml'] = "True"
        return self


    def stop(self):
        self.unwrap_target_method()
        if self.show_calls:
            del environ['show_rest_calls'    ]
        if self.show_xml:
            del environ['show_rest_calls_xml']
        if self.show_calls or self.show_xml:
            print("#######################################################")
            print("##### Stopped showing SOAP calls to /sdk endpoint #####")
            print("#######################################################")
            print()
        return self

    def wrap_target_method(self):
        self.wrap_method = Hook_Method(self.target_module, self.target_method)
        self.wrap_method.add_on_before_call(self.before_call)
        self.wrap_method.add_on_after_call (self.after_call)
        self.wrap_method.wrap()

    def unwrap_target_method(self):
        self.wrap_method.unwrap()