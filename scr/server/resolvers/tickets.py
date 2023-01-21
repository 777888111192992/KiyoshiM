from src.server.base.dbmanager import base_worker
from src.server.base.models import Ticket


def get(ticket_id: int) -> dict:
    res = base_worker.execute_query(query="SELECT id, zoo_id, user_id, date "
                                          "FROM tickets "
                                          "WHERE id=?",
                                    args=(ticket_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"
        return res

    res["result"] = Ticket(
        id=res["result"][0],
        zoo_id=res["result"][1],
        user_id=res["result"][2],
        date=res["result"][3]
    )

    return res


def create(ticket: Ticket) -> dict[str: int, str: str, str: Ticket]:
    res = \
        base_worker.execute_query(query="INSERT INTO tickets(zoo_id, user_id, date) "
                                        "VALUES (?, ?, ?)"
                                        "RETURNING id",
                                  args=(ticket.zoo_id, ticket.user_id, ticket.date,))

    if res["result"] is not None:
        res["result"] = get(ticket_id=res["result"][0])["result"]

    return res


def get_all() -> dict:
    res = base_worker.execute_query(
        query="SELECT id, zoo_id, user_id, date FROM tickets",
        fetch_one=False)

    list_tickets = []

    if res["result"]:
        for ticket in res["result"]:
            list_tickets.append(Ticket(
                id=ticket[0],
                zoo_id=ticket[1],
                user_id=ticket[2],
                date=ticket[3]
            ))

    if not list_tickets:
        res["result"] = "No cities"
    else:
        res["result"] = list_tickets

    return res


def update(ticket_id: int, new_data: Ticket) -> dict:
    res = base_worker.execute_query(query="UPDATE tickets "
                                          "SET (zoo_id, user_id, date) = (?, ?, ?) "
                                          "WHERE id=?"
                                          "RETURNING id",
                                    args=(new_data.zoo_id, new_data.user_id, new_data.date, ticket_id))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found/Incorrect data"
    elif type(res["result"]) == tuple:
        res["result"] = get(ticket_id=res["result"][0])["result"]
    else:
        res["code"] = 400
        res["message"] = "Undefined error"

    return res


def delete(ticket_id: int) -> dict:
    res = base_worker.execute_query(query="DELETE FROM tickets WHERE id=? RETURNING id",
                                    args=(ticket_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"

    return res
