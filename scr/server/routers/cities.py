from fastapi import APIRouter, Response
from src.server.base.models import City
from src.server.resolvers import cities

router = APIRouter(prefix='/cities', tags=["Cities"])


@router.get(path="/", response_model=str)
def start_page() -> str:
    return "start page"


@router.post(path="/new", status_code=200, response_model=dict)
def new(responce: Response, city: City) -> dict:
    res = cities.create(city=city)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get/{city_id}", status_code=200, response_model=dict)
def get(responce: Response, city_id: int) -> dict:
    res = cities.get(city_id=city_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get_all", status_code=200, response_model=dict)
def get_all(responce: Response) -> dict:
    res = cities.get_all()
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.put(path="/update/{city_id}", response_model=dict, status_code=200)
def update(responce: Response, city_id: int, new_data: City) -> dict:
    res = cities.update(city_id=city_id, new_data=new_data)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.delete(path="/delete/{city_id}", status_code=200, response_model=dict)
def delete(responce: Response, city_id: int) -> dict:
    res = cities.delete(city_id=city_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res
