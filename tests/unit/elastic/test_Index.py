from pprint import pprint
from osbot_elastic.helpers.TestCase_Index import TestCase_Index


class test_Index(TestCase_Index):

    def setUp(self) -> None:
        pass

    def test_list(self):
        indexes_ids = set(self.index.list(index_by='index'))
        assert '.opendistro_security' in indexes_ids
        assert self.index_id          in indexes_ids


    def test_info(self):
        assert set(self.index.info()) == {'settings', 'mappings', 'aliases'}

    #todo add support for index patterns
        # for index pattern
        # pprint(self.elastic.es.cat.indices(format="json") )

        # self.result = self.elastic.create_index_pattern()._result
        # self.elastic.index = 'test-index*'
        # self.elastic.delete_index_pattern()
        #self.result = self.elastic._result
