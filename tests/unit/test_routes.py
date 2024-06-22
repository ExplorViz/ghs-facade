import unittest
from unittest.mock import patch, MagicMock
from ghs_facade import app 

class TestUpdateMergeRequest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    @patch('ghs_facade.gl.projects.get')
    def test_update_merge_request(self, mock_get):
        # Mock the Project and MergeRequest objects from the GitLab API
        mock_project = MagicMock()
        mock_merge_request = MagicMock(description='Old Description')
        
        # Set the return values of the mock objects
        mock_get.return_value = mock_project
        mock_project.mergerequests.get.return_value = mock_merge_request
        
        # Define the payload to send to the endpoint
        payload = {
            'merge_request_id': '1',
            'project_id': '123',
            'explorviz_url': 'http://example.com'
        }
        
        # Make a POST request to the endpoint
        response = self.app.post('/update_merge_request', json=payload)
        
        # Verify the status code and response
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Merge request updated successfully.' in response.get_data(as_text=True))
        
        # Ensure the GitLab API was called as expected
        mock_get.assert_called_once_with('123')
        mock_project.mergerequests.get.assert_called_once_with('1')
        
        # Check that the merge request description was updated correctly
        new_description = 'Old Description\n\nExplorViz URL: http://example.com'
        self.assertEqual(mock_merge_request.description, new_description)

    @patch('os.environ.get')
    @patch('ghs_facade.gl.projects.get')
    def test_no_payload_uses_env_vars(self, mock_get, mock_env):
        # Mock environment variables
        mock_env.side_effect = lambda x: {'CI_MERGE_REQUEST_IID': '1', 'CI_MERGE_REQUEST_PROJECT_ID': '123', 'DEFAULT_EXPLORVIZ_URL': 'http://example.com'}.get(x)

        # Mock the Project and MergeRequest objects from the GitLab API
        mock_project = MagicMock()
        mock_merge_request = MagicMock(description='Old Description')
        mock_get.return_value = mock_project
        mock_project.mergerequests.get.return_value = mock_merge_request

        # Make a POST request to the endpoint without payload
        response = self.app.post('/update_merge_request', json={})

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn('Merge request updated successfully.', response.get_data(as_text=True))
        mock_get.assert_called_once_with('123')
        mock_project.mergerequests.get.assert_called_once_with('1')
        self.assertIn('http://example.com', mock_merge_request.description)

    @patch('os.environ.get')
    def test_error_when_essential_params_missing_and_no_env_vars(self, mock_env):
        # Mock environment variables to return None
        mock_env.return_value = None

        # Make a POST request to the endpoint without sufficient data and no env vars
        response = self.app.post('/update_merge_request', json={})

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required parameters.', response.get_data(as_text=True))

    @patch('os.environ.get')
    @patch('ghs_facade.gl.projects.get')
    def test_partial_payload_supplemented_by_env_vars(self, mock_get, mock_env):
        # Mock environment variables for missing payload data
        mock_env.side_effect = lambda x: {'CI_MERGE_REQUEST_PROJECT_ID': '123'}.get(x)

        # Mock the Project and MergeRequest objects from the GitLab API
        mock_project = MagicMock()
        mock_merge_request = MagicMock(description='Old Description')
        mock_get.return_value = mock_project
        mock_project.mergerequests.get.return_value = mock_merge_request

        # Define partial payload
        payload = {
            'merge_request_id': '1',
            'explorviz_url': 'http://example.com'
        }

        # Make a POST request to the endpoint with partial payload
        response = self.app.post('/update_merge_request', json=payload)

        # Assertions for behavior with environment variable supplementation
        self.assertEqual(response.status_code, 200)
        self.assertIn('Merge request updated successfully.', response.get_data(as_text=True))
        mock_get.assert_called_once_with('123')  # Project ID from env var
        mock_project.mergerequests.get.assert_called_once_with('1')
        self.assertIn('http://example.com', mock_merge_request.description)

class TestGetProjects(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    @patch('ghs_facade.gl.projects.list')
    def test_get_project(self, mock_get):
        mock_project = MagicMock(project_id="id", name="Testproject")

        mock_get.return_value = mock_project

        response = self.app.get("/get_project/Testproject")

        self.assertEqual(response.status_code, 200)
        
        mock_get.assert_called_once_with(get_all=True, search="Testproject")

    @patch('ghs_facade.gl.projects.list')
    def test_get_all_projects(self, mock_get):
        mock_project = MagicMock(project_id="id", name="Testproject")

        mock_get.return_value = mock_project

        response = self.app.get("/get_all_projects")

        self.assertEqual(response.status_code, 200)
        
        mock_get.assert_called_once_with(get_all=True)
    
    @patch('ghs_facade.gl.projects.get')
    def test_create_issue(self, mock_get):
        mock_project = MagicMock()
        mock_issue = MagicMock(title="Testtitle", description="Testdescription")
        

        mock_get.return_value = mock_project
        mock_project.issue.create.return_value = mock_issue

        response = self.app.post("/create_issue", json={"project_id": "id", "title": "Testtitle", "description": "Testdescription"})

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully created Issue', response.get_data(as_text=True))
    
    def test_create_issue_when_params_missing(self):

        response = self.app.post("/create_issue", json={"title": "Testtitle", "description": "Testdescription"})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required parameters.', response.get_data(as_text=True))

        response = self.app.post("/create_issue", json={})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required parameters.', response.get_data(as_text=True))
        
if __name__ == '__main__':
    unittest.main()
