from fastapi import APIRouter, Response
from src.server.base.models import User, UserLogin
from src.server.resolvers import users

router = APIRouter(prefix='/users', tags=["Users"])


@router.get(path="/", response_model=str)
def start_page() -> str:
    return "start page"


@router.post(path="/new", status_code=200, response_model=dict)
def new(responce: Response, user: User) -> dict:
    res = users.create(user=user)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get/{user_id}", status_code=200, response_model=dict)
def get(responce: Response, user_id: int) -> dict:
    res = users.get(user_id=user_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get_all", status_code=200, response_model=dict)
def get_all(responce: Response) -> dict:
    res = users.get_all()
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.put(path="/update/{user_id}", response_model=dict, status_code=200)
def update(responce: Response, user_id: int, new_data: User) -> dict:
    res = users.update(user_id=user_id, new_data=new_data)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.delete(path="/delete/{user_id}", status_code=200, response_model=dict)
def delete(responce: Response, user_id: int) -> dict:
    res = users.delete(user_id=user_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/login", response_model=dict, status_code=200)
def check_login(responce: Response, user: UserLogin) -> dict:
    res = users.check_login(user=user)
    if res["code"] != 200:
        responce.status_code = 400
    return res
