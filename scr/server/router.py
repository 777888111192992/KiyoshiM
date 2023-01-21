from src.server.routers import personnel, zoos, users, cities, tickets

routers = (personnel.router, zoos.router, users.router, cities.router, tickets.router)
