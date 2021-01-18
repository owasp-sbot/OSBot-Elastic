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

    def test_container_run(self):
        assert 'Hello from Docker!'  in self.es_docker.container_run('hello-world')

    def test_containers(self):
        assert type(self.es_docker.containers()) is list            # todo once we create a container per execution change this to reflect that

    def test_images(self):
        images = self.es_docker.images()
        assert len(images) > 0

    def test_images_names(self):
        names = self.es_docker.images_names()
        assert 'hello-world:latest' in names

    def test_image_pull(self):
        images_config      = Env().get_docker_images_config()
        image_config       = images_config.get('elastic_search')
        (repository, tag)   = (image_config.get('repository'), image_config.get('tag'))
        image_name         = f"{repository}:{tag}"

        image              = self.es_docker.image_pull(repository, tag)
        assert image.tags == ['docker.elastic.co/elasticsearch/elasticsearch:7.10.1', 'elasticsearch:7.10.1']


        assert self.es_docker.container_run(image_name,"pwd") == "/usr/share/elasticsearch"

    def test_server_info(self):
        server_info = self.es_docker.server_info()
        assert 'KernelMemory' in server_info
        assert lower(server_info.get('OSType')) == 'linux'
