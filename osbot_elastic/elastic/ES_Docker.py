import docker
from docker.errors import ImageNotFound

from osbot_elastic.Env import Env
from osbot_elastic.api.API_Docker import API_Docker
from osbot_elastic.helpers._to_add_to_osbot.OSBot_Utils__Local import bytes_to_string, trim


class ES_Docker(API_Docker):

    # def __init__(self):
    #     super().__init__(self)

    def config_image(self, image_name):
        images_config      = Env().get_docker_images_config()
        image_config       = images_config .get(image_name)
        repository         = image_config  .get('repository')
        tag                = image_config  .get('tag')
        return {    'repository' : repository          ,
                    'tag'        : tag                 ,
                    'name'       : f'{repository}:{tag}'

        }

    def download_image_elastic_search(self):
        return self.download_image('elastic_search')

    def download_image(self, image_name):
        config = self.config_image(image_name)
        self.image_pull(config.get('repository'), config.get('tag'))
        return config.get('name') in self.images_names()
