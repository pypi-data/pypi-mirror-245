import os
import requests

def get_stored_api_key():
    home_dir = os.path.expanduser('~')
    api_key_file = os.path.join(home_dir, '.sigiq_api_key')
    try:
        with open(api_key_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception("API key not found. Please run 'sigiq-login' to set your API key.")


def call_gpt(model_params):
    api_key = get_stored_api_key()
    url = "http://35.247.56.152/call-gpt/"

    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "api_key": api_key,
        "model_params": model_params,
    }

    response = requests.get(url, json=payload, headers=headers)
    return response.json()

def get_stats(user=None):
    api_key = get_stored_api_key()
    url = "http://35.247.56.152/get-stats/"
    
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "api_key": api_key,
    }
    if user:
        payload['user'] = user

    response = requests.get(url, json=payload, headers=headers)
    return response.json()