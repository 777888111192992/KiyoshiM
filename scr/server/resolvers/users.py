import sqlite3

from src.server.base.dbmanager import base_worker
from src.server.base.models import User, UserLogin


def get(user_id: int) -> dict:
    res = base_worker.execute_query(query="SELECT id, login, password, power_level "
                                          "FROM users "
                                          "WHERE id=?",
                                    args=(user_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"
        return res

    res["result"] = User(
        id=res["result"][0],
        login=res["result"][1],
        password=res["result"][2],
        power_level=res["result"][3]
    )

    return res


def create(user: User) -> dict:
    res = \
        base_worker.execute_query(query="INSERT INTO users(login, password, power_level) "
                                        "VALUES (?, ?, ?)"
                                        "RETURNING id",
                                  args=(user.login, user.password, user.power_level))

    if res["result"] is not None:
        res["result"] = get(user_id=res["result"][0])["result"]

    return res


def get_all() -> dict:
    res = base_worker.execute_query(
        query="SELECT id, login, password, power_level FROM users",
        fetch_one=False)

    list_users = []

    if res["result"]:
        for user in res["result"]:
            list_users.append(User(
                id=user[0],
                login=user[1],
                password=user[2],
                power_level=user[3]
            ))

    if not list_users:
        res["result"] = "No users"
    else:
        res["result"] = list_users

    return res


def update(user_id: int, new_data: User) -> dict:
    old_user = get(user_id)["result"]
    res = base_worker.execute_query(query="UPDATE users "
                                          "SET (login, password, power_level) = (?, ?, ?) "
                                          "WHERE id=?"
                                          "RETURNING id",
                                    args=(new_data.login, new_data.password, new_data.power_level, user_id))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found/Incorrect data"
        return res
    user = get(res["result"][0])["result"]
    # if old_user == user:
    #     res["result"] = None
    #     res["code"] = 400
    #     res["message"] = "Duplicate data"
    #     return res
    if type(res["result"]) == tuple:
        res["result"] = user
    else:
        res["code"] = 400
        res["message"] = "Undefined error"
        return res

    return res


def delete(user_id: int) -> dict:
    res = base_worker.execute_query(query="DELETE FROM users WHERE id=? RETURNING id",
                                    args=(user_id,))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"

    return res


def check_login(user: UserLogin) -> dict:
    res = base_worker.execute_query(query="SELECT id, login, password, power_level FROM users WHERE (login, password) = (?, ?)",
                                    args=(user.login, user.password))

    if res["result"] is None:
        res["code"] = 400
        res["message"] = "Not found"
        return res

    res["result"] = User(
        id=res["result"][0],
        login=res["result"][1],
        password=res["result"][2],
        power_level=res["result"][3]
    )

    return res
