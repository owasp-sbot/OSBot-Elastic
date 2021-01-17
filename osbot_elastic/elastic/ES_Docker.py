import docker

from osbot_elastic.helpers._to_add_to_osbot.OSBot_Utils__Local import bytes_to_string


class ES_Docker:

    def __init__(self):
        self.client = docker.from_env()

    def container_run(self, image, command=None):
        output = self.client.containers.run(image, command)
        return bytes_to_string(output)

    def containers(self):
        return self.client.containers.list()



    def server_info(self):
        return self.client.info()