from flask import Flask
from flask_cors import CORS
import os
import gitlab

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Configuration for GitLab
PERSONAL_ACCESS_TOKEN = os.environ.get('PERSONAL_ACCESS_TOKEN')
if not PERSONAL_ACCESS_TOKEN:
    raise ValueError("The 'PERSONAL_ACCESS_TOKEN' environment variable is not set.")

GITLAB_API_URL = os.environ.get('GITLAB_API_URL', 'https://gitlab.com')

# Initialize GitLab
gl = gitlab.Gitlab(GITLAB_API_URL, private_token=PERSONAL_ACCESS_TOKEN)

from .routes import *