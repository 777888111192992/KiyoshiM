from fastapi import APIRouter, Response
from src.server.base.models import Ticket
from src.server.resolvers import tickets

router = APIRouter(prefix='/tickets', tags=["Tickets"])


@router.get(path="/", response_model=str)
def start_page() -> str:
    return "start page"


@router.post(path="/new", status_code=200, response_model=dict)
def new(responce: Response, ticket: Ticket) -> dict:
    res = tickets.create(ticket=ticket)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get/{ticket_id}", status_code=200, response_model=dict)
def get(responce: Response, ticket_id: int) -> dict:
    res = tickets.get(ticket_id=ticket_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.get(path="/get_all", status_code=200, response_model=dict)
def get_all(responce: Response) -> dict:
    res = tickets.get_all()
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.put(path="/update/{ticket_id}", response_model=dict, status_code=200)
def update(responce: Response, ticket_id: int, new_data: Ticket) -> dict:
    res = tickets.update(ticket_id=ticket_id, new_data=new_data)
    if res["code"] != 200:
        responce.status_code = 400
    return res


@router.delete(path="/delete/{ticket_id}", status_code=200, response_model=dict)
def delete(responce: Response, ticket_id: int) -> dict:
    res = tickets.delete(ticket_id=ticket_id)
    if res["code"] != 200:
        responce.status_code = 400
    return res
