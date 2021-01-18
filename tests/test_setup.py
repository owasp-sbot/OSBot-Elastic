from unittest import TestCase

class test_setup(TestCase):

    def test_setup(self):
        pass


def setUpModule():
    print('-----\n********')        # todo: add code to start ES docker
    print("setup_module")

def tearDownModule():
    print('-----\n********')        # todo: add code to stop ES docker
    print("tearDownModule")