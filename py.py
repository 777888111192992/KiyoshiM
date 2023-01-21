import requests
from src.server.base.models import User
import settings


def register(user: User) -> dict:
    answer = requests.post(
        url=f'{settings.URL}/users/new',
        data=f'{{ "login": "{user.login}", "password": "{user.password}", "power_level": "{user.power_level}" }}').json()
    return answer


register(User(
    login="1",
    password="1",
    power_level=1
))