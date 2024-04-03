## Requirements
- Python 3.12.2

## Startup

1. Activate virtual environment (Optional, but recommended)

   `foo@bar:~$ source ci_facade_env/bin/activate`

2. Install dependencies

    `foo@bar:~$ pip install -r requirements.txt`

3. Run Flask app

    `foo@bar:~$ python run.py`

4. Deactivate virtual environment

    `foo@bar:~$ deactivate`

5. Update requirements.txt

    If you installed a library, update the `requirements.txt` file via `foo@bar:~$ pip3 freeze > requirements.txt`