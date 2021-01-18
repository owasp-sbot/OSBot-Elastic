import os
from unittest                    import TestCase
import pytest

from osbot_elastic.Env import Env


class test_Env(TestCase):

    def setUp(self):
        self.env = Env()

    @pytest.mark.usefixtures('fixtures')
    def test_get_elastic_server_config(self):
        with self.monkeypatch.context() as m:
            m.setenv("ELASTIC_SERVER"   , 'host')
            m.setenv("ELASTIC_KIBANA"   , 'kibana')
            m.setenv("ELASTIC_PORT"     , 'port')
            m.setenv("ELASTIC_USERNAME" , 'username')
            m.setenv("ELASTIC_PASSWORD" , 'password')
            assert self.env.get_elastic_server_config() == { "host"    : "host"     ,
                                                             "kibana"  : "kibana"   ,
                                                             "password": "password" ,
                                                             "port"    : "port"     ,
                                                             "username": "username" }
    @pytest.mark.usefixtures('fixtures')
    def test_get_docker_images_config(self):
        with self.monkeypatch.context() as m:
            m.setenv("DOCKER_IMAGE_ELASTIC_SEARCH", 'repository')
            m.setenv("DOCKER_TAG_ELASTIC_SEARCH", 'tag')
            assert self.env.get_docker_images_config() == { 'elastic_search': { 'repository': 'repository',
                                                                                'tag'       : 'tag' } }
            m.delenv("DOCKER_IMAGE_ELASTIC_SEARCH")
            m.delenv("DOCKER_TAG_ELASTIC_SEARCH"  )
            assert self.env.get_docker_images_config() == { 'elastic_search': { 'repository': 'docker.elastic.co/elasticsearch/elasticsearch',
                                                                                'tag'       : '7.10.1' } }

    # add pytest features to self
    @pytest.fixture(autouse=False)
    def fixtures(self, capsys, monkeypatch, tmpdir):
        self.capsys      = capsys                       # captures print statements
        self.monkeypatch = monkeypatch                  # set and restore object values
        self.tmpdir      = tmpdir                       # use temp dirs