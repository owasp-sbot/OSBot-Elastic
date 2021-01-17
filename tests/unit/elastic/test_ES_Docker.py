from pprint import pprint
from unittest import TestCase

from osbot_elastic.elastic.ES_Docker import ES_Docker
from osbot_elastic.helpers._to_add_to_osbot.OSBot_Utils__Local import sorted_set, bytes_to_string


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
        assert sorted_set(self.es_docker.server_info()) == ['Architecture', 'BridgeNfIp6tables', 'BridgeNfIptables', 'CPUSet', 'CPUShares', 'CgroupDriver', 'ClusterAdvertise', 'ClusterStore', 'ContainerdCommit',
                                                            'Containers', 'ContainersPaused', 'ContainersRunning', 'ContainersStopped', 'CpuCfsPeriod', 'CpuCfsQuota', 'Debug', 'DefaultRuntime', 'DockerRootDir',
                                                            'Driver', 'DriverStatus', 'ExperimentalBuild', 'GenericResources', 'HttpProxy', 'HttpsProxy', 'ID', 'IPv4Forwarding', 'Images', 'IndexServerAddress',
                                                            'InitBinary', 'InitCommit', 'Isolation', 'KernelMemory', 'KernelMemoryTCP', 'KernelVersion', 'Labels', 'LiveRestoreEnabled', 'LoggingDriver', 'MemTotal',
                                                            'MemoryLimit', 'NCPU', 'NEventsListener', 'NFd', 'NGoroutines', 'Name', 'NoProxy', 'OSType', 'OomKillDisable', 'OperatingSystem', 'PidsLimit', 'Plugins',
                                                            'ProductLicense', 'RegistryConfig', 'RuncCommit', 'Runtimes', 'SecurityOptions', 'ServerVersion', 'SwapLimit', 'Swarm', 'SystemStatus', 'SystemTime', 'Warnings']

