from os import environ

from dotenv import load_dotenv

class Env():
    def __init__(self):
        load_dotenv()

    def get_elastic_server_config(self):
        return {
                    "host"    : environ.get('ELASTIC_SERVER'),
                    "kibana"  : environ.get('ELASTIC_KIBANA'),
                    "port"    : environ.get('ELASTIC_PORT'),
                    "username": environ.get('ELASTIC_USERNAME'),
                    "password": environ.get('ELASTIC_PASSWORD')
                }

    def get_docker_images_config(self):
        return {
                    "elastic_search" : environ.get('DOCKER_IMAGE_ELASTIC_SEARCH')
        }
