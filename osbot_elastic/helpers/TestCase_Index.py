from unittest import TestCase

from osbot_utils.utils.Misc import random_string

from osbot_elastic.Elastic_Search import Elastic_Search
from osbot_elastic.api.Index import Index
from osbot_elastic.elastic.ES import ES


class TestCase_Index(TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        cls.es       = ES().setup()
        cls.index    = Index(es=cls.es)
        cls.index_id = cls.index.index_id
        assert cls.index_id not in cls.index.list_names()
        assert cls.index.create() == {'acknowledged': True, 'index': cls.index_id, 'shards_acknowledged': True}
        assert cls.index_id in cls.index.list_names()

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.index_id in cls.index.list_names()
        assert cls.index.delete() == {'acknowledged': True}
        assert cls.index_id not in cls.index.list_names()