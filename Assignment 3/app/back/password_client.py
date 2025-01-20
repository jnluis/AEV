from typing import Union
import requests

from django.conf import settings

PASS_SERVICE_HOST = f"http://{settings.PASS_SERVICE_ADDR}:{settings.PASS_SERVICE_PORT}"

def get_all_passwords() -> Union[list, None]:
    response = requests.get(f"{PASS_SERVICE_HOST}/")
    if response.status_code == 200:
        return response.json()
    return None

def get_password(pass_id: int) -> Union[dict, None]:
    response = requests.get(f"{PASS_SERVICE_HOST}/{pass_id}")
    if response.status_code == 200:
        return response.json()
    return None

def create_password(password: str) -> Union[dict, None]:
    response = requests.post(f"{PASS_SERVICE_HOST}/", json={"password": password})
    if response.status_code == 200:
        return response.json()
    return None

def update_password(pass_id: int, password: str) -> Union[dict, None]:
    response = requests.put(f"{PASS_SERVICE_HOST}/{pass_id}", json={"password": password})
    if response.status_code == 200:
        return response.json()
    return None

def delete_password(pass_id: int) -> Union[dict, None]:
    response = requests.delete(f"{PASS_SERVICE_HOST}/{pass_id}")
    if response.status_code == 200:
        return response.json()
    return None