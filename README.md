# Git Hosting Service Facade (ghs-facade)

The ghs-facade provides an HTTP API used by ExplorViz to access Git hosting services' APIs, e.g., GitLab.
For example, ExplorViz's [code-service](https://github.com/explorviz/code-service) uses this facade to insert the URL to the ExplorViz [frontend](https://github.com/explorviz/frontend) in the description of a given merge request.

## Requirements
- Python >= 3.12.2
- A `PERSONAL_ACCESS_TOKEN` that has been registered for a user in GitLab.

## Usage
- Local: `PERSONAL_ACCESS_TOKEN=<INSERT_PERSONAL_ACCESS_TOKEN> GITLAB_API_URL=<INSERT_URL> python3 app.py`
- Docker: `docker run -d -p 5050:80 -e PERSONAL_ACCESS_TOKEN=ypCa3Dzb23o5nvsixwPA -e GITLAB_API_URL=http://localhost:8345 explorviz/ghs-facade:latest`

## Development

1. Activate virtual environment (Optional, but recommended)

   `foo@bar:~$ source ghs_facade_env/bin/activate`

2. Install dependencies

    `foo@bar:~$ pip3 install -r requirements.txt`

3. Run Flask app

    `foo@bar:~$ python3 app.py`

4. Deactivate virtual environment

    `foo@bar:~$ deactivate`

5. Update requirements.txt

    If you installed a library, update the `requirements.txt` file via `foo@bar:~$ pip3 freeze > requirements.txt`

### Helpful development workflow

- Run Dockerized Gitlab-CE with predefined user and access token: `docker run -d -p 8345:80 explorviz/build-images:gitlab-ce` (username `root@local`, pw `hhn<hkbS1C@?FZC%0hIX`, https://git.se.informatik.uni-kiel.de/ExplorViz/code/ci-images/-/tree/main/gitlab-ce?ref_type=heads)

- Run tests against an Gitlab-CE (for example against the one previous started): `PERSONAL_ACCESS_TOKEN=ypCa3Dzb23o5nvsixwPA GITLAB_API_URL=http://localhost:8345 pytest tests/integration`
  - This will create a project and a merge request: http://localhost:8345/root/test-project/-/merge_requests/1 that can now be used and do not need to be manually created
   - This step is optional. If not executed you need to create a project and merge request that can be modified.

- Run ghs-facade that uses the Dockerized Gitlab-CE (and is pre-configured):

  `PERSONAL_ACCESS_TOKEN=ypCa3Dzb23o5nvsixwPA -e GITLAB_API_URL=http://localhost:8345 explorviz/ghs-facade:latest` 

  or 
  
  `PERSONAL_ACCESS_TOKEN=ypCa3Dzb23o5nvsixwPA GITLAB_API_URL=http://localhost:8345 CI_MERGE_REQUEST_IID=1 CI_MERGE_REQUEST_PROJECT_ID=1 DEFAULT_EXPLORVIZ_URL=http://localhost:4200 python3 app.py`

- Update merge request description with
  
  `curl -v -H 'Content-Type: application/json' -d '{"merge_request_id":"1","project_id":"1", "explorviz_url":"http://localhost:4200"}' -X POST http://localhost:5000/update_merge_request`

  or

  `curl -v -H 'Content-Type: application/json' -X POST http://localhost:5000/update_merge_request`

## Testing

- Integration tests: `PERSONAL_ACCESS_TOKEN=ypCa3Dzb23o5nvsixwPA GITLAB_API_URL=http://localhost:8345 pytest tests/integration`

- Unit tests: `PERSONAL_ACCESS_TOKEN=ypCa3Dzb23o5nvsixwPA GITLAB_API_URL=http://localhost:8345 pytest tests/unit`

### Potential Problems

- This is probably not a problem, but might occur on some Docker Client updates: During the integration tests, a dependency of testcontainers uses the `/var/run/docker.sock` to retrieve data about containers. Therefore, it is essential to have a symbolic link from `/var/run/docker.sock` to the Docker socket file typically located at `$HOME/.docker/run/docker.sock` for the integration tests to function correctly.