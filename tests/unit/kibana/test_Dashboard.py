#todo: fix test (this is the code from the original cdr_plugin_folder_to_folder repo)

# from unittest import TestCase
# from unittest.mock import Mock, patch, MagicMock
#
# class test_Dashboard(TestCase):
#
#     def setUp(self):
#         self.host = self.config.kibana_host
#         self.port = self.config.kibana_port
#         self.kibana = Kibana(host=self.host, port=self.port).setup()
#         self.kibana.enabled = True
#
#         self.dashboard_name = 'temp_dashboard'
#         self.dashboard = Dashboard(kibana=self.kibana, dashboard_name=self.dashboard_name)
#
#     # def test_create_info_exists_delete(self):
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Dashboard.Dashboard.exists')
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana.requests.post')
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana.json.loads')
#     def test_create_dashboard(self, mock_loads, mock_post, mock_exists):
#         mock_loads.return_value = True
#         mock_post.return_value.ok = True
#         mock_exists.return_value = False
#
#         result = self.dashboard.create()
#         assert result
#
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana.Kibana.index_patterns')
#     def test_dashboard_exists_info(self, mock_patterns):
#         result = self.dashboard.exists()
#         assert result
#
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Dashboard.Dashboard.info')
#     def test_id(self, mock_info):
#         mock_info.return_value = {'id': "Successful"}
#         result = self.dashboard.id()
#         assert result == "Successful"
#
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Dashboard.Dashboard.exists')
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Dashboard.Dashboard.id')
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana.Kibana.delete_request')
#     def test_dashboard_delete(self, mock_delete, mock_id, mock_exists):
#         mock_delete.return_value = True
#         mock_id.return_value = True
#         mock_exists.return_value = False
#
#         assert self.dashboard.delete()
#
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Dashboard.Dashboard.info')
#     def test_dashboard_delete_no_object(self, mock_info):
#         mock_info.return_value = {"error": "Dashboard object not found."}
#
#         assert self.dashboard.delete() == False
#
#     @patch('osbot_utils.utils.Http.GET')
#     @patch('osbot_utils.utils.Files.file_create')
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana.requests.post')
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana.json.loads')
#     def test_import_dashboard_github(self, mock_loads, mock_post, mock_create, mock_get):
#         mock_loads.return_value = True
#         mock_post.return_value.text = "Successful!"
#         mock_create.return_value = True
#         mock_get.return_value = True
#         import_result = self.dashboard.import_dashboard_from_github(dashboard_file_name='processed-files-v8.ndjson')
#         assert import_result == "Successful!"
#
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana.requests.post')
#     def test_export_dashboard(self, mock_post):
#         mock_post.return_value.text = 'd73d7220-ab6f-11eb-b1b2-a1d32a234c46'
#         dashboard_id = 'd73d7220-ab6f-11eb-b1b2-a1d32a234c46'
#         dashboard = Dashboard(kibana=self.kibana, dashboard_id=dashboard_id)
#         export_data = dashboard.export_dashboard()
#         assert dashboard_id in export_data
#
#     @patch('cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Elastic.Kibana.requests.post')
#     def test_export_not_existing_dashboard(self, mock_post):
#         mock_post.return_value.text = "404. Not found."
#         dashboard_id = 'ffdd80b7-11eb-4dd9-b8ce-293254a5c961'
#         dashboard = Dashboard(kibana=self.kibana, dashboard_id=dashboard_id)
#         export_data = dashboard.export_dashboard()
#         assert '404' in export_data