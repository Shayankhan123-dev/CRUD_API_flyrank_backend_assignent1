# Task API - FastAPI CRUD (Dockerized)

A simple CRUD (Create, Read, Update, Delete) REST API built with FastAPI for the FlyRank Backend Assignment.

*Update: This project has now been fully containerized using Docker (Podman) and uses a persistent SQLite database mounted via Docker volumes.*

## Features

- Create a task
- View all tasks
- View a single task
- Update a task
- Delete a task
- Interactive Swagger documentation
- **Docker Containerization** (App and database environment run in isolated containers)
- **Data Persistence** (Data survives server and container restarts via Docker volumes)

---

## Proving the Architecture

A major goal of this assignment was to swap the storage layer and deployment method without breaking the API. 
**The service and routes remained 100% unchanged.** The clients sending `GET`, `POST`, `PUT`, and `DELETE` requests experience the exact same behavior, proving the value of decoupling the API layer from the storage/infrastructure layer.

### How Persistence was Proven
Data persistence was verified across container restarts using the following steps:
1. Sent a `POST /tasks` request to create a task named "Docker persistence test".
2. Ran `docker compose down` to completely destroy the running containers.
3. Ran `docker compose up -d` to spin up fresh containers.
4. Sent a `GET /tasks` request and verified that "Docker persistence test" was still present, proving the `sqlite_data` Docker volume successfully protected the database file.

---

## Getting Started (Docker / Podman)

The easiest way to run this project is using Docker Compose.

**1. Clone the repository**
```bash
git clone [https://github.com/Shayankhan123-dev/CRUD_API_flyrank_backend_assignent1.git](https://github.com/Shayankhan123-dev/CRUD_API_flyrank_backend_assignent1.git)
cd CRUD_API_flyrank_backend_assignent1