import  json
import  datetime
import  requests
from dotenv import load_dotenv
from    elasticsearch                           import Elasticsearch, helpers, NotFoundError
from    osbot_aws.apis.Secrets                  import Secrets
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from    requests.auth                           import HTTPBasicAuth
from    osbot_utils.utils.Http                  import DELETE
# todo: find long term solution for this (including being able to detect it)
# on 25 August 2020, GWBot needed this fix
#note the max query value in the search has been increased from 10000 to 100000 (which will need to be done on any new ES Install)
# PUT _all/_settings
# {
# "index.max_result_window" : "100000"
# }
from osbot_elastic.elastic.Index import Index
from osbot_elastic.elastic.ES import ES
from osbot_utils.utils.Misc import env_vars


class Elastic_Search:
    def __init__(self, index, aws_secret_id = None):
        #self.timestamp      = datetime.datetime.utcnow()
        self.index          = index
        self.aws_secret_id  = aws_secret_id
        self.kibana         = None
        self.host           = None
        self.port           = None
        self.scheme         = None
        self._result        = None                          # used to cache some responses (for methods that return self)
        self.es             = None
        #self._setup()


    def _setup(self):
        if self._setup_elastic_on_cloud_via_aws_secret() is False:
            if self._setup_elastic_using_env_vars() is False:
                self._setup_elastic_on_localhost()
        return self

    # # todo refactor to ES class
    # def _setup_using_env_variables(self):
    #     self.es = ES().setup()
    #     return self

    def _setup_elastic_on_localhost(self):
        self.host   = 'localhost'
        self.port   = 9200
        self.scheme = 'http'
        self.es     = Elasticsearch([{'host': self.host, 'port': self.port}])

    def _setup_elastic_on_cloud_via_aws_secret(self,):
        index     = self.index
        secret_id = self.aws_secret_id
        if secret_id:
            credentials = json.loads(Secrets(secret_id).value())
            self.kibana = credentials.get('kibana')
            self.host   = credentials['host']
            username    = credentials['username']
            password    = credentials['password']
            port        = credentials['port']
            self.index  = index
            self._setup_Elastic_on_cloud(self.host, port, username, password)
            return True
        return False

    def _setup_elastic_using_env_vars(self):
        load_dotenv()
        vars     = env_vars()
        username = vars.get('ELASTIC_USERNAME', 'elastic' )
        password = vars.get('ELASTIC_PASSWORD'            )
        server   = vars.get('ELASTIC_SERVER' , '127.0.0.1')
        port     = vars.get('ELASTIC_PORT'   , '9200'     )
        ssl_cert = vars.get('ELASTIC_SSL_CERT'            )
        if username and server and port:
            self._setup_Elastic_on_cloud(server=server, port = port, username=username, password=password)
            return True
        return False

    def _setup_Elastic_on_cloud(self, server, port, username, password, scheme='https', ssl_cert=None):
        self.server        = server
        self.port          = port
        self.scheme        = scheme
        self.host          = f"{scheme}://{self.server}:{self.port}"
        ssl_cert           = ssl_cert
        self.es            = Elasticsearch(hosts                  = [self.host],
                                           http_auth              = (username, password),
                                           ssl_assert_fingerprint = ssl_cert)
        return self

    @cache_on_self
    def api_index(self):
        api_index = Index(self.es, self.index)
        self.index = api_index.index_id                     # handle fact that in this api index variable was used to hold the index_id
        return api_index

    def add_data_with_timestamp(self,data, refresh=False):
        data["@timestamp"] = datetime.datetime.utcnow() #self.timestamp
        return self.es.index(index=self.index, doc_type='item', body=data, refresh=refresh)

    def add(self,data, id_key = None, pipeline=None, refresh=False):
        api_index = self.api_index()
        api_index.pipeline = pipeline
        return api_index.add(data=data, id_key=id_key, refresh=refresh)

    def add_bulk(self, data, id_key = None, pipeline = None, refresh=True):
        api_index = self.api_index()
        api_index.pipeline = pipeline
        return api_index.add(data=data, id_key=id_key, refresh=refresh)
        # ok = 0
        # if data:
        #     actions = []
        #     for item in data:
        #         item_data = {
        #                         "_index": self.index,
        #                         "_type": 'item',
        #                         "_source": item,
        #                     }
        #         if id_key is not None:
        #             item_data["_id"] = item[id_key]
        #         actions.append(item_data)
        #
        #     if pipeline is None:
        #         ok, _ = helpers.bulk(self.es, actions, index=self.index)
        #     else:
        #         ok, _ = helpers.bulk(self.es, actions, index=self.index, pipeline=pipeline)
        # return ok

    def create_index(self,extra_kwargs = None):
        if self.exists() is False:
            self._result = self.api_index().create()
        return self

    def create_index_with_location_geo_point(self,field = "location"):
        body = {
                "mappings": {
                    "item": {
                        "properties": {
                            field: {
                                "type": "geo_point"
                            }
                        }
                    }
                }
            }
        self.create_index(body)
        return self

    def create_index_pattern(self, time_field = None):
        if time_field:
            payload = {"attributes":{"title": self.index ,"fields":"[]", f"timeFieldName": f"{time_field}"}}
        else:
            payload= {"attributes":{"title": self.index ,"fields":"[]"}}
        data     = json.dumps(payload)
        headers  = {'Content-Type': 'application/json', 'kbn-xsrf' : 'kibana'}
        url      = f'https://{self.kibana}:{self.port}/api/saved_objects/index-pattern' # todo refactor into POST method
        response = requests.post(url, data, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
        self._result = json.loads(response.text)
        return self

    def delete_index(self):
        if self.exists():
            self._result = self.api_index().delete_index()
        return self

    def delete_index_pattern(self):
        try:
            if self.host == 'localhost':
                url = 'http://{0}:{1}/.kibana/doc/index-pattern:{2}'.format(self.host,self.port, self.index)
                self._result = json.loads(DELETE(url))
            else:
                #not working, will need to use something like /api/saved_objects/index-pattern/784b1a30-3931-11ea-a5e9-45b5e8966813
                url = 'https://{0}:{1}/.kibana/doc/index-pattern:{2}'.format(self.host, self.port, self.index)
                response = requests.delete(url, auth=HTTPBasicAuth(self.username, self.password))
                self._result = json.loads(response.text)
        except Exception as error:
            self._result = { 'error':  error}
        return self

    def delete_data_by_id(self, id, refresh=False):
        try:
            return self.es.delete(index=self.index, id=id, refresh=refresh)
        except Exception as error:
            return { 'error':  error }

    @cache_on_self
    def elastic(self):          # use this to get a cached version of this class (Elastic_Search) that is fully configured
        if self.es is None:
            self._setup()
        return self

    def get_data(self,id):
        try:
            return self.es.get(index=self.index, id=id)
        except NotFoundError:
            return None

    def get_many(self, ids):
        data = self.es.mget(index=self.index, body={'ids': ids})
        results = {}
        for item in data['docs']:
            _id = item['_id']
            if item['found'] is False:
                results[_id] = None
            else:
                results[_id] = item['_source']
        return results

    def get_data_First_10(self):
        results = self.es.search(index=self.index, body={"query": {"match_all": {}}})
        for result in results['hits']['hits']:
            yield result['_source']

    def get_index_settings(self):
        url = 'https://{3}:{4}@{0}:{1}/{2}/_settings'.format(self.host, self.port, self.index, self.username, self.password)
        return json.loads(requests.get(url).text)

    def get_data_between_dates(self,field, from_date,to_date):
        query = {"query": { "range": { field: { "gte": from_date,
                                                "lt" : to_date     } }}}
        return list(self.search_using_query(query))

    def last_execution_result(self):
        return self._result

    def search_using_lucene(self, query, size=100000, sort = None):              # for syntax and examples of lucene queries see https://www.elastic.co/guide/en/elasticsearch/reference/6.4/query-dsl-query-string-query.html#query-string-syntax
        query = query.replace('“', '"').replace('”','"')                        # fix the quotes we receive from Slack
        results = self.es.search(index=self.index, q=query, size=size,sort = sort)
        for result in results['hits']['hits']:
            yield result['_source']

    def search_using_lucene_index_by_id(self, query, size=100000, sort = None):  # for syntax and examples of lucene queries see https://www.elastic.co/guide/en/elasticsearch/reference/6.4/query-dsl-query-string-query.html#query-string-syntax
        query = query.replace('“', '"').replace('”','"')                        # fix the quotes we receive from Slack
        elk_results = self.es.search(index=self.index, q=query, size=size, sort= sort)
        results = {}
        for result in elk_results['hits']['hits']:
            id          = result['_id']
            value       = result['_source']
            results[id] = value
        return results

    def search_using_lucene_sort_by_date(self, query, size=100000, sort="date:desc"):     # todo need better solution for the use of 100000 , needed by one of the projects      # for syntax and examples of lucene queries see https://www.elastic.co/guide/en/elasticsearch/reference/6.4/query-dsl-query-string-query.html#query-string-syntax
        query = query.replace('“', '"').replace('”','"')                        # fix the quotes we receive from Slack
        elk_results = self.es.search(index=self.index, q=query, size=size, sort=sort)
        results = []
        for result in elk_results['hits']['hits']:
            id          = result['_id']
            value       = result['_source']
            item        = { "id":id , "value": value}
            results.append(item)
        return results

    def search_using_query(self, query, size = 100000):  # for GWBot making this 100k # to be more that 10000 this needs a Elastic change
        results = self.es.search(index=self.index, body= query, size=size)
        for result in results['hits']['hits']:
            yield result['_source']

    def search_on_field_for_value(self, field, value, size=100000):
        query = {"query": {"match": { field : {"query": value}}}}
        return self.search_using_query(query, size=size)

    def search_on_field_for_values(self, field, values):
        query = {"query": { "constant_score": { "filter": { "terms": { field: values } } } } }
        return self.search_using_query(query)

    # this is not working
    # def search_get_unique_field_values(self, field,size = 10000):
    #     query = {
    #         "size": 0,
    #         "aggs": {
    #             "unique_ids": {
    #                 "terms": {
    #                     "field": 'field',
    #                     "size": size
    #                 }
    #             }
    #         }
    #     }
    #     return self.search_using_query(query)


    def set_index_settings(self, settings):
        headers = {'Content-Type': 'application/json'}
        url = 'https://{0}:{1}/{2}/_settings'.format(self.host, self.port, self.index)
        response = requests.put(url, json.dumps(settings), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
        return response.text

    def set_index_settings_total_fields(self,value):
        self.set_index_settings({"index.mapping.total_fields.limit": value})
        return self

    def url(self):
       return f'{self.scheme}://{self.host}:{self.port}'

    def delete_using_query(self, query):
        results = self.es.delete_by_query(index=self.index, body=query)
        return results

    def index_list(self):
        return self.api_index().list_names()#

    def info(self):
        return self.es.info()

    def exists(self):
        return self.api_index().exists()

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
        return self
