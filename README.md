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

### Helpful commands

`PERSONAL_ACCESS_TOKEN=<INSERT_PERSONAL_ACCESS_TOKEN> GITLAB_API_URL=<INSERT_URL> CI_MERGE_REQUEST_IID=1 CI_MERGE_REQUEST_PROJECT_ID=1 DEFAULT_EXPLORVIZ_URL=http://localhost:4200 python3 app.py`

`curl -H 'Content-Type: application/json' -X POST http://localhost:5000/update_merge_request`

## Testing

- Integration tests: `PERSONAL_ACCESS_TOKEN=ypCa3Dzb23o5nvsixwPA GITLAB_API_URL=http://localhost:8345 pytest tests/integration`

- Unit tests: `PERSONAL_ACCESS_TOKEN=ypCa3Dzb23o5nvsixwPA GITLAB_API_URL=http://localhost:8345 pytest tests/unit`