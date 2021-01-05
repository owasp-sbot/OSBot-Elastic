import os
from unittest                    import TestCase

from osbot_elastic.Env import Env


class test_Env(TestCase):

    def setUp(self):
        self.env = Env()

    def test_elastic_credentials(self):
        assert type(os.environ['ELASTIC_SERVER'       ]) is str
        assert type(os.environ['ELASTIC_USERNAME'     ]) is str
        assert type(os.environ['ELASTIC_PASSWORD'     ]) is str

    def test_get_elastic_server_config(self):
        assert set(self.env.get_elastic_server_config()) == {'host', 'password', 'username', 'port'}