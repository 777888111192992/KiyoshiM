from src.server.base.dbmanager import base_worker
from src.server.base.models import Person


def get(person_id: int) -> dict:
    res = base_worker.execute_query(query="SELECT id, surname, post_id, name, patronymic, date_birth "
                                          "FROM personnel "
                                          "WHERE id=?",
                                    args=(person_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"
        return res

    res["result"] = Person(
        id=res["result"][0],
        surname=res["result"][1],
        post_id=res["result"][2],
        name=res["result"][3],
        patronymic=res["result"][4],
        date_birth=res["result"][5]
    )

    return res


def create(person: Person) -> dict:
    res = \
        base_worker.execute_query(query="INSERT INTO personnel(name, surname, post_id, patronymic, date_birth) "
                                        "VALUES (?, ?, ?, ?, ?)"
                                        "RETURNING id",
                                  args=(person.name, person.surname, person.post_id, person.patronymic,
                                        person.date_birth))

    if res["result"] is not None:
        res["result"] = get(person_id=res["result"][0])["result"]

    return res


def get_all() -> dict:
    res = base_worker.execute_query(
        query="SELECT id, surname, post_id, name, patronymic, date_birth FROM personnel",
        fetch_one=False)

    list_personnel = []

    if res["result"]:
        for person in res["result"]:
            list_personnel.append(Person(
                id=person[0],
                surname=person[1],
                post_id=person[2],
                name=person[3],
                patronymic=person[4],
                date_birth=person[5]
            ))

    if not list_personnel:
        res["result"] = "No staff"
    else:
        res["result"] = list_personnel

    return res


def update(person_id: int, new_data: Person) -> dict:
    old_person = get(person_id)
    res = base_worker.execute_query(query="UPDATE personnel "
                                          "SET (name, surname, post_id, date_birth, patronymic) = (?, ?, ?, ?, ?) "
                                          "WHERE id=?"
                                          "RETURNING id",
                                    args=(new_data.name, new_data.surname, new_data.post_id, new_data.date_birth,
                                          new_data.patronymic, person_id))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found/Incorrect data"
        return res

    if old_person["result"] == get(res["result"][0])["result"]:
        res["result"] = None
        res["code"] = 400
        res["message"] = "Duplicate data"
    elif type(res["result"]) == tuple:
        res["result"] = get(person_id=res["result"][0])["result"]
    else:
        res["code"] = 400
        res["message"] = "Undefined error"

    return res


def delete(person_id: int) -> dict:
    res = base_worker.execute_query(query="DELETE FROM personnel WHERE id=? RETURNING id",
                                    args=(person_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"

    return res
