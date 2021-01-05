
#from osbot_aws.helpers.Test_Helper import Test_Helper
from pprint import pprint
from unittest import TestCase

from osbot_elastic.Elastic_Search import Elastic_Search

#Test_Helper
class Test_Elastic_Search(TestCase):

    def setUp(self):
        self.index     = 'test-index'
        #self.secret_id = 'gw-elastic-server-1'

        self.elastic = Elastic_Search(self.index)._setup_using_env_variables()#, aws_secret_id=self.secret_id)
        self.result = None

    def tearDown(self) -> None:
        if self.result is not None:
            pprint(self.result)

    def test__setup_using_env_variables(self):
        #self.elastic.setup_using_env_variables()
        assert '.opendistro_security' in self.elastic.index_list()

    def test_add(self):
        pass
        # self.elastic.add({'answer':42})

    def test_create_index_delete_index_list_index(self):
        assert self.index not in self.elastic.index_list()
        assert self.elastic.create_index()._result == {'acknowledged': True, 'index': self.index, 'shards_acknowledged': True}
        assert self.index in self.elastic.index_list()

        #self.result = self.elastic.create_index_pattern()._result
        #self.elastic.index = 'test-index*'
        #self.elastic.delete_index_pattern()
        assert self.elastic.delete_index()._result == {'acknowledged': True}
        assert self.index not in self.elastic.index_list()
        #self.result = self.elastic._result

    def test_index_pattern(self):
        pass

    def test_info(self):
        info = self.elastic.es.info()
        assert info['tagline'] == 'You Know, for Search'
        list(set(info)) == ['version', 'tagline', 'cluster_name', 'cluster_uuid', 'name']

    def test_test_info(self):
        assert '.apm-agent-configuration' in self.elastic.index_list()

    def test_add_data_with_timestamp(self):
        data    = { 'answer' : 42}
        response = self.elastic.add_data_with_timestamp(data)
        assert response.get("_index") == self.elastic.index

    def test_index_list(self):
        self.result = self.elastic.index_list()

    def test_search_using_query(self):
        term = 'jira'
        query =  {"query": { "wildcard": { "Summary": term}}}
        result = list(self.elastic.search_using_query(query))

        assert term in result.pop(0)['Summary'].lower()
        assert len(result) > 20


    def test_test_search_using_query___large_query(self):
        query = {"_source": ["Key", "Issue Links"], }

        result = list(self.elastic.set_index('sec_project').search_using_query(query))
        Dev.pprint(len(result))

    def test_get_data_between_dates(self):
        results = self.elastic.get_data_between_dates("Created", "now-1d", "now")
        Dev.pprint(len(results))
        for issue in results:
            print(issue.get('Summary'))


    def test_index_list(self):
        assert 'jira' in self.elastic.index_list()

    def test_search_using_lucene(self):
        #query = "Summary:jira"
        query = 'Project:RISK AND Status:"Fixed"'
        self.index = "*"
        results = list(self.elastic.search_using_lucene(query))

        #for issue in results:
        #    print('{0:10} {1:10} {2:20} {3}'.format(issue.get('Key'), issue.get('Project'),issue.get('Status'),issue.get('Summary')))

        assert len(results) > 100

    def test_search_using_lucene____Issue_with_Epic(self):
        self.elastic.index = 'it_assets'
        query = '"GSOKR-924"'
        results = list(self.elastic.search_using_lucene(query))
        assert len(results) == 25