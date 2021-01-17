from pprint import pprint
from unittest import TestCase

from osbot_elastic.elastic.ES_Docker import ES_Docker
from osbot_elastic.helpers._to_add_to_osbot.OSBot_Utils__Local import sorted_set, bytes_to_string, lower


class test_ES_Docker(TestCase):

    def setUp(self) -> None:
        self.es_docker = ES_Docker()
        print()

    def test__init__(self):
        assert type(self.es_docker.client).__name__ == 'DockerClient'

    def test_container_run(self):
        assert 'Hello from Docker!'  in self.es_docker.container_run('hello-world')

    def test_containers(self):
        assert type(self.es_docker.containers()) is list            # todo once we create a container per execution change this to reflect that

    def test_server_info(self):
        server_info = self.es_docker.server_info()
        assert 'KernelMemory' in server_info
        assert lower(server_info.get('OSType'        )) == 'linux'
