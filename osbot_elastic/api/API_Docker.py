import docker

from osbot_elastic.helpers._to_add_to_osbot.OSBot_Utils__Local import bytes_to_string, trim

class API_Docker:

    def __init__(self):
        self.client = docker.from_env()

    def container_run(self, repository, tag=None, command=None):
        if tag:
            image = f"{repository}:{tag}"
        else:
            image = repository
        try:
            output = self.client.containers.run(image, command)
            return { 'status': 'ok'   , 'output' : trim(bytes_to_string(output)) }
        except Exception as exception:
            return { 'status': 'error', 'error': f'{exception}', 'exception': exception  }

    def containers(self):
        return self.client.containers.list()

    def image_elastic_search(self):
        return

    def image_pull(self, repository, tag):
        return self.client.images.pull(repository, tag)

    def images(self):
        return self.client.images.list()

    def images_names(self):
        names = []
        for image in self.images():
            for tag in image.tags:
                names.append(tag)
        return sorted(names)

    def server_info(self):
        return self.client.info()