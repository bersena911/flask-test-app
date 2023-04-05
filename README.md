## Install Requirements

```shell
pip install -r requirements.txt
```

### Environment file
You must have environment file with correct values to run server properly, here is example

```text
DB_URI=postgresql://postgres:testtest@localhost:5432/postgres

BACKEND_CORS_ORIGINS=http://localhost, http://localhost:8000
SECRET_KEY=some_secret_key # can be generated using openssl
FIRST_SUPERUSER=admin@test.com
FIRST_SUPERUSER_PASSWORD=testtest
```

### Run Migrations before running server

```shell
alembic upgrade head
```


### Run development server
```shell
python app.py
```

After first run it will create superuser based on .env file