from src.server.base.dbmanager import base_worker
from src.server.base.models import City


def get(city_id: int) -> dict:
    res = base_worker.execute_query(query="SELECT id, title "
                                          "FROM cities "
                                          "WHERE id=?",
                                    args=(city_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"
        return res

    res["result"] = City(
        id=res["result"][0],
        title=res["result"][1]
    )

    return res


def create(city: City) -> dict:
    res = \
        base_worker.execute_query(query="INSERT INTO cities(title) "
                                        "VALUES (?)"
                                        "RETURNING id",
                                  args=(city.title,))

    if res["result"] is not None:
        res["result"] = get(city_id=res["result"][0])["result"]

    return res


def get_all() -> dict:
    res = base_worker.execute_query(
        query="SELECT id, title FROM cities",
        fetch_one=False)

    list_cities = []

    if res["result"]:
        for city in res["result"]:
            list_cities.append(City(
                id=city[0],
                title=city[1]
            ))

    if not list_cities:
        res["result"] = "No cities"
    else:
        res["result"] = list_cities

    return res


def update(city_id: int, new_data: City) -> dict:
    res = base_worker.execute_query(query="UPDATE cities "
                                          "SET (title) = (?) "
                                          "WHERE id=?"
                                          "RETURNING id",
                                    args=(new_data.title, city_id))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found/Incorrect data"
    elif type(res["result"]) == tuple:
        res["result"] = get(city_id=res["result"][0])["result"]
    else:
        res["code"] = 400
        res["message"] = "Undefined error"

    return res


def delete(city_id: int) -> dict:
    res = base_worker.execute_query(query="DELETE FROM cities WHERE id=? RETURNING id",
                                    args=(city_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"

    return res
