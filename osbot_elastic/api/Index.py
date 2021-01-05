from elasticsearch import Elasticsearch
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Misc import random_string


class Index:
    def __init__(self,es : Elasticsearch, index_id=None):
        self.es = es
        self.index_id = index_id or random_string(prefix='index_')

    def create(self,body=None):
        if self.exists() is False:
            body = body or {}
            return self.es.indices.create(index=self.index_id, body=body)
        return { 'error':  f'index {self.index_id} already existed, nothind done'}

    def delete(self):
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