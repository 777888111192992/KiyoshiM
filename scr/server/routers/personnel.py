from fastapi import APIRouter, Response
from src.server.base.models import Person
from src.server.resolvers import personnel

router = APIRouter(prefix='/personnel', tags=["Personnel"])


@router.get(path="/", response_model=str)
def start_page() -> str:
    return "start page"


@router.post(path="/new", response_model=dict)
def new(responce: Response, person: Person) -> dict:
    res = personnel.create(person=person)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get/{person_id}", status_code=200, response_model=dict)
def get(responce: Response, person_id: int) -> dict:
    res = personnel.get(person_id=person_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get_all", status_code=200, response_model=dict)
def get_all(responce: Response) -> dict:
    res = personnel.get_all()
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.put(path="/update/{person_id}", response_model=dict, status_code=200)
def update(responce: Response, person_id: int, new_data: Person) -> dict:
    res = personnel.update(person_id=person_id, new_data=new_data)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.delete(path="/delete/{person_id}", status_code=200, response_model=dict)
def delete(responce: Response, person_id: int) -> dict:
    res = personnel.delete(person_id=person_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res
