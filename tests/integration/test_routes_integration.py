import time
import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from ghs_facade import app, gl
import logging
import socket 

LOGGER = logging.getLogger(__name__)

GITLAB_PORT = 8345

@pytest.fixture(scope="session")
def gitlab_container():


    isPortFree = socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('localhost', GITLAB_PORT)) != 0
    
    container = DockerContainer("explorviz/build-images:gitlab-ce")

    if isPortFree:
        LOGGER.info("Port is not allocated. Will now start a Gitlab CE instance.")
        container.with_bind_ports(80, GITLAB_PORT)
        container.start()

        # Wait for GitLab to be up. This might need adjustment based on your system's performance.
        wait_for_logs(container, "Server initialized", timeout=300)

        LOGGER.info("Server seems to be running. Tests will start in 20 seconds.")
        time.sleep(20)
    
    else:
        LOGGER.info("Port is already allocated. GitLab CE is probably running. Will run tests against this running instance.")

    # Create project
    LOGGER.info("Creating dummy project and merge request")
    root = gl.users.list(username='root')[0]
    root_project = root.projects.create({'name': 'test-project'})

    project = gl.projects.get("root/test-project")

    project.files.create(
        {
            "file_path": "README.md",
            "branch": "main",
            "content": "data to be written",
            "encoding": "text",  # or 'base64'; useful for binary files
            "commit_message": "Create file",
        }
    )

    project.branches.create({'branch': 'feature1', 'ref': 'main'})

    project.mergerequests.create({'source_branch': 'feature1', 'target_branch': 'main', 'title': 'merge cool feature', 'description': 'New description'})

    # Return the container object for use in tests
    yield container

    # Cleanup after tests are done
    if isPortFree:
        container.stop(delete_volume=True, force=True)

def test_update_merge_request(gitlab_container):

    testApp = app.test_client()
    testApp.testing = True

    project_name_with_namespace = "root/test-project"
    project = gl.projects.get(project_name_with_namespace)

    assert project is not None

    flask_app_url = "http://localhost:5000/update_merge_request"
    
    # Extract the merge request ID for the test
    merge_requests = project.mergerequests.list()
    assert len(merge_requests) > 0, "No merge requests found in the project."
    merge_request_id = merge_requests[0].get_id()

    explorviz_url = "http://example.com/explorviz_url"

    # Data to be sent to Flask app
    data = {
        "merge_request_id": merge_request_id,
        "project_id": project.id,
        "explorviz_url": explorviz_url
    }

    # Make the POST request to the Flask app
    response = testApp.post(flask_app_url, json=data)

    # Assert response status code and message
    assert response.status_code == 200
    assert 'Merge request updated successfully.' in response.get_data(as_text=True)

    updated_mr = project.mergerequests.get(merge_request_id)

    # Check GitLab merge request
    assert f"ExplorViz URL: {explorviz_url}" in updated_mr.attributes.get("description")

