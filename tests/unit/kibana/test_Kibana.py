from unittest import TestCase

from osbot_elastic.kibana.Kibana import Kibana
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Http import GET
from osbot_utils.utils.Misc import list_set


class test_Kibana(TestCase):

    def setUp(self):
        self.kibana = Kibana().setup()

    def test_data_views(self):
        pprint(self.kibana.data_views())

    def test_data_view_create(self):
        title   = "logstash-*"
        name    = "My Logstash Data View"
        data_view = self.kibana.data_views(index_by='name').get(name)
        if data_view is None:
            result = self.kibana.data_view_create(index_pattern=title, name=name)
            data_view = result.get('data_view')
        assert self.kibana.data_view_exists(name=name) is True
        assert data_view.get('name' ) == name
        assert data_view.get('title') == title
        view_id = data_view.get('id')

        assert self.kibana.data_view_delete(view_id=view_id) == True
        assert self.kibana.data_view_exists(name=name      ) is False


    def test_dashboards(self):
        pprint(self.kibana.dashboards())

    def test_features(self):
        pprint(self.kibana.features())


    def test_setup(self):
        self.kibana.setup()
        assert self.kibana.enabled is True

    def test_request_url(self):
        result = GET(self.kibana.request_url())
        assert 'kibana' in result