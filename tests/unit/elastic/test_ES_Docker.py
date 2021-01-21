from pprint import pprint
from unittest import TestCase

from osbot_elastic.Env import Env
from osbot_elastic.elastic.ES_Docker import ES_Docker
from osbot_elastic.helpers._to_add_to_osbot.OSBot_Utils__Local import sorted_set, bytes_to_string, lower


class test_ES_Docker(TestCase):

    def setUp(self) -> None:
        self.es_docker = ES_Docker()
        print()

    def test__init__(self):
        assert type(self.es_docker.client).__name__ == 'DockerClient'



    def test_download_image_elastic_search(self):
        assert self.es_docker.download_image_elastic_search() is True

        #assert  'docker.elastic.co/elasticsearch/elasticsearch:7.10.1' in image.tags
        #assert self.es_docker.container_run(repository, tag,"pwd") == {'output': '/usr/share/elasticsearch', 'status': 'ok'}

    def test_server_info(self):
        server_info = self.es_docker.server_info()
        assert 'KernelMemory' in server_info
        assert lower(server_info.get('OSType')) == 'linux'
