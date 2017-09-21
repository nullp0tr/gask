import json
import os
from .utils.gauth import SessionManager

home_path = os.path.expanduser('~')
try:
    with open(home_path + '/.gask/conf.json') as file:
        data = json.load(file)
except FileNotFoundError:
    data = dict(url='http://127.0.0.1:8000')

url = data['url']
login_suffix = '/api-auth/login/'
session_manager = SessionManager(url=url, login_suffix=login_suffix)
