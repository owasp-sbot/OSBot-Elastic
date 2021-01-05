from pprint import pprint
from unittest import TestCase
from osbot_elastic.Elastic_Search import Elastic_Search



class test_Index(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.index_id = 'test-index'
        cls.elastic = Elastic_Search(cls.index_id)._setup_using_env_variables()
        cls.index = cls.elastic.api_index()

        assert cls.index_id not in cls.index.list_names()
        assert cls.index.create() == {'acknowledged': True, 'index': cls.index_id, 'shards_acknowledged': True}
        assert cls.index_id in cls.index.list_names()

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.index.delete() == {'acknowledged': True}
        assert cls.index_id not in cls.index.list_names()

    def setUp(self) -> None:
        pass


    def test_list(self):
        pprint(self.elastic.es.indices.get_alias())
        indexes_ids = set(self.index.list(index_by='index'))
        assert '.opendistro_security' in indexes_ids
        assert self.index_id          in indexes_ids


    def test_info(self):
        print()
        pprint(self.index.info())
        # for index pattern
        # pprint(self.elastic.es.cat.indices(format="json") )

        # self.result = self.elastic.create_index_pattern()._result
        # self.elastic.index = 'test-index*'
        # self.elastic.delete_index_pattern()
        #self.result = self.elastic._result
