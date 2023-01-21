from src.server.base.dbmanager import base_worker
from src.server.base.models import Zoo


def get(zoo_id: int) -> dict:
    res = base_worker.execute_query(query="SELECT id, title, phone, city_id "
                                          "FROM zoo "
                                          "WHERE id=?",
                                    args=(zoo_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"
        return res

    res["result"] = Zoo(
        id=res["result"][0],
        title=res["result"][1],
        phone=res["result"][2],
        city_id=res["result"][3]
    )

    return res


def create(zoo: Zoo) -> dict:
    res = \
        base_worker.execute_query(query="INSERT INTO zoo(title, phone, city_id) "
                                        "VALUES (?, ?, ?)"
                                        "RETURNING id",
                                  args=(zoo.title, zoo.phone, zoo.city_id))

    if res["result"] is not None:
        res["result"] = get(zoo_id=res["result"][0])["result"]

    return res


def get_all() -> dict:
    res = base_worker.execute_query(
        query="SELECT id, title, phone, city_id FROM zoo",
        fetch_one=False)

    list_zoo = []

    if res["result"]:
        for zoo in res["result"]:
            list_zoo.append(Zoo(
                id=zoo[0],
                title=zoo[1],
                phone=zoo[2],
                city_id=zoo[3]
            ))

    if not list_zoo:
        res["result"] = "No zoos"
    else:
        res["result"] = list_zoo

    return res


def update(zoo_id: int, new_data: Zoo) -> dict:
    res = base_worker.execute_query(query="UPDATE zoo "
                                          "SET (title, phone, city_id) = (?, ?, ?) "
                                          "WHERE id=?"
                                          "RETURNING id",
                                    args=(new_data.title, new_data.phone, new_data.city_id, zoo_id))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found/Incorrect data"
    elif type(res["result"]) == tuple:
        res["result"] = get(zoo_id=res["result"][0])["result"]
    else:
        res["code"] = 400
        res["message"] = "Undefined error"

    return res


def delete(zoo_id: int) -> dict:
    res = base_worker.execute_query(query="DELETE FROM zoo WHERE id=? RETURNING id",
                                    args=(zoo_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"
        
    return res
