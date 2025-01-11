##  Microservice: Analysis of financial transactions

### Usage

Project Language: Python 3.12.3

Project Framework: FastAPI 0.110.1


### Installation Steps:
```bash
git  clone

pip install poetry

poetry install

poetry shell
```

### Database Migrations
```bash
alembic upgrade head
```

### Running Locally
```bash

# server
uvicorn main:app --reload

# celery
celery -A src.common.celery worker --loglevel=info
```


### Running with Docker Compose
```bash
docker compose up --build
```

### Running Tests
```bash
pytest
```

### Running Tests With Coverage

```bash
coverage run -m pytest
```

### Running Tests with Docker Compose
```bash

docker compose -f docker-compose.unittest.yaml up --build --abort-on-container-exit

```
