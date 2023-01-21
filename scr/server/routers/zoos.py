from fastapi import APIRouter, Response
from src.server.base.models import Zoo
from src.server.resolvers import zoos

router = APIRouter(prefix='/zoos', tags=["Zoos"])


@router.get(path="/", response_model=str)
def start_page() -> str:
    return "start page"


@router.post(path="/new", status_code=200, response_model=dict)
def new(responce: Response, zoo: Zoo) -> dict:
    res = zoos.create(zoo=zoo)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get/{zoo_id}", status_code=200, response_model=dict)
def get(responce: Response, zoo_id: int) -> dict:
    res = zoos.get(zoo_id=zoo_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get_all", status_code=200, response_model=dict)
def get_all(responce: Response) -> dict:
    res = zoos.get_all()
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.put(path="/update/{zoo_id}", response_model=dict, status_code=200)
def update(responce: Response, zoo_id: int, new_data: Zoo) -> dict:
    res = zoos.update(zoo_id=zoo_id, new_data=new_data)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.delete(path="/delete/{zoo_id}", status_code=200, response_model=dict)
def delete(responce: Response, zoo_id: int) -> dict:
    res = zoos.delete(zoo_id=zoo_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res
