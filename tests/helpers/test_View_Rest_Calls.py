from pprint import pprint
from unittest import TestCase

from osbot_elastic.Elastic_Search import Elastic_Search
from osbot_elastic.helpers.View_Rest_Calls import View_Rest_Calls


class test_View_Rest_Calls(TestCase):

    def test____enter______exit__(self):
        with View_Rest_Calls() as view_rest_calls:
            elastic = Elastic_Search(None)._setup_using_env_variables()
            print()
            elastic.index_list()
            elastic.exists()

