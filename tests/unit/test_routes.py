import unittest
from unittest.mock import patch, MagicMock
from githost_service import app 

class TestUpdateMergeRequest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    @patch('githost_service.gl.projects.get')
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
        mock_get.assert_called_once_with('123', lazy=True)
        mock_project.mergerequests.get.assert_called_once_with('1', lazy=True)
        
        # Check that the merge request description was updated correctly
        new_description = 'Old Description\n\nExplorViz URL: http://example.com'
        self.assertEqual(mock_merge_request.description, new_description)
        
if __name__ == '__main__':
    unittest.main()
