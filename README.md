## Requirements
- Python 3.12.2

## Startup

1. Activate virtual environment (Optional, but recommended)

   `foo@bar:~$ source ghs_facade_env/bin/activate`

2. Install dependencies

    `foo@bar:~$ pip install -r requirements.txt`

3. Run Flask app

    `foo@bar:~$ python run.py`

4. Deactivate virtual environment

    `foo@bar:~$ deactivate`

5. Update requirements.txt

    If you installed a library, update the `requirements.txt` file via `foo@bar:~$ pip3 freeze > requirements.txt`

## Development

`PERSONAL_ACCESS_TOKEN=glpat-REeaU-oVWoPBAziQu6p7 GITLAB_API_URL=http://localhost:8080 CI_MERGE_REQUEST_IID=1 CI_MERGE_REQUEST_PROJECT_ID=1 DEFAULT_EXPLORVIZ_URL=http://localhost:4200 python3 run.py`

`curl -H 'Content-Type: application/json' -d '{"login":"my_login","password":"my_password"}' -X POST http://localhost:5000/update_merge_request`