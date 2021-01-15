from pprint import pprint
from unittest import TestCase
from unittest.mock import patch, call

from osbot_elastic.Elastic_Search import Elastic_Search
from osbot_elastic.helpers.View_Rest_Calls import View_Rest_Calls


class test_View_Rest_Calls(TestCase):

    @patch('builtins.print')
    def test____enter______exit__(self,builtins_print):
        with View_Rest_Calls() as view_rest_calls:
            elastic = Elastic_Search(None)._setup_using_env_variables()
            assert len(view_rest_calls.calls) == 0
            elastic.index_list()
            assert len(view_rest_calls.calls) == 1
            elastic.exists()
            assert len(view_rest_calls.calls) == 2
        view_rest_calls.print_calls_made()

        calls = builtins_print.mock_calls

        assert len(calls) == 8

        pprint(calls)
        assert calls[0] == call()
        assert calls[1] == call('#######################################################')
        assert calls[2] == call('##### REST calls made to Elastic Server           #####')
        assert calls[3] == call('#######################################################')
        assert calls[4] == call()
        assert calls[5] == call('Method   Url                  Params    ')
        assert calls[6] == call("GET      /_cat/indices        {'format': b'json'}")
        assert calls[7] == call(f'HEAD     /{elastic.api_index().index_id}        {{}}        ')



