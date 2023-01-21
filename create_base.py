import src.client.api.resolvers
from src.server.base.dbmanager import base_worker
from settings import SQL_SCRIPTS_DIR


if __name__ == "__main__":
    base_worker.create_base(file=f"{SQL_SCRIPTS_DIR}/tables.sql")


@src.client.api.resolvers.server_available
def connect_check():
    return src.client.api.resolvers.server_available()


def aboba():
    if {"message"} == "Server not available" in connect_check():
        print('Server not available')
    return None


print(aboba())
print(connect_check())