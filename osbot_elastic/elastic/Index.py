from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Misc import random_string


class Index:
    def __init__(self, es : Elasticsearch, index_id=None):
        self.es       = es
        self.doc_type = 'item'
        self.index_id  = index_id or random_string(prefix='temp_index_').lower()

    def add(self,data, id_key = None, refresh=False):
        if data is None or data == {}:
            return {'error': 'no data provided to send to ELK'}
        try:
            if id_key is not None:
                return self.es.index(index=self.index_id, doc_type=self.doc_type, body=data, refresh=refresh, id=data[id_key])
            else:
                return self.es.index(index=self.index_id, doc_type=self.doc_type, body=data, refresh=refresh                 )
        except Exception as error:
            message = f'in Elastic_Search:add: {error}'
            print(message)
            return {"elk-error": "{0}".format(message)}

    def create(self,body=None):
        if self.exists() is False:
            body = body or {}
            return self.es.indices.create(index=self.index_id, body=body)
        return { 'error':  f'index {self.index_id} already existed, nothind done'}

    def data(self, **kwargs):
        return self.data_query({"match_all": {}}, **kwargs)

    @index_by
    @group_by
    def data_query(self, query):
        for item in scan(self.es, index=self.index_id, doc_type=self.doc_type, query={"query": query}):
            yield item.get('_source')

    def delete(self, id, refresh=False):
        try:
            return self.es.delete(index=self.index_id, doc_type=self.doc_type, id=id, refresh=refresh)
        except Exception as error:
            return { 'error':  error }

    def delete_index(self):
        if self.exists():
            return self.es.indices.delete(self.index_id)
        return { 'warning':  f"index {self.index_id} didn't exist, nothind done"}

    def exists(self):
        return self.es.indices.exists(self.index_id)

    def info(self):
        data = self.es.indices.get(index=self.index_id)
        return data.get(self.index_id)

    @index_by
    @group_by
    def list(self):
        return self.es.cat.indices(format="json")

    def list_names(self):
        return list(set(self.list(index_by='index')))