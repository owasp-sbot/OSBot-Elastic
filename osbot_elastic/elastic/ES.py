from elasticsearch import Elasticsearch
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from osbot_elastic.Env import Env


class ES:

    def __init__(self):
        self.http_compress = True               # todo: refactor to 'default_options' object
        self.scheme        = 'https'

    def setup_using_env_variables(self):
        server_config      = Env().get_elastic_server_config()
        self.host          = server_config['host'    ]
        self.kibana        = server_config['kibana'  ]
        self.username      = server_config['username']
        self.password      = server_config['password']
        self.port          = server_config['port'    ]


        return Elasticsearch(hosts         = [self.host]                   ,
                             http_compress = self.http_compress            ,
                             http_auth     = (self.username, self.password),
                             scheme        = self.scheme                   ,
                             port          = self.port )

    @cache_on_self
    def setup(self):
        return self.setup_using_env_variables()  # todo add support for the other setup modes