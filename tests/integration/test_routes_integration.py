import time
import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from ghs_facade import gl
import logging

LOGGER = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def gitlab_container():

    # This uses the official GitLab Docker image. Adjust the version as needed.
    container = DockerContainer("explorviz/build-images:gitlab-ce")
    container.with_bind_ports(80, 8345)
    container.start()


    # Wait for GitLab to be up. This might need adjustment based on your system's performance.
    wait_for_logs(container, "Server initialized", timeout=240)

    LOGGER.info("Server seems to be running. Tests will start in 20 seconds.")
    time.sleep(20)

    # Create project
    LOGGER.info("Creating dummy project")
    root = gl.users.list(username='root')[0]
    user_project = root.projects.create({'name': 'test-project'})
    user_projects = root.projects.list()

    # Return the container object for use in tests
    yield container

    # Cleanup after tests are done
    container.stop(delete_volume=True, force=True)

def test_update_merge_request(gitlab_container):
    project_name_with_namespace = "root/test-project"
    project = gl.projects.get(project_name_with_namespace)

    assert project is not None