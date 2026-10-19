# Databases — Docker credentials and configuration lab

Fork this repository to complete [DevOps Lab 4](https://github.com/WaqasSaleem97/DevOps_F26/tree/main/Labs/Lab04). Run the application and databases through Docker Compose. Python and its database drivers are installed inside the application image.

The lab demonstrates four stages:

| Stage | Program | Configuration source |
| --- | --- | --- |
| 1 | `01_mysql_hardcoded.py` | Hardcoded MySQL endpoint and credentials |
| 2 | `02_mongo_hardcoded.py` | Hardcoded MongoDB endpoint and credentials |
| 3 | `03_mongo_env.py` | Process environment variables for dev, test and prod |
| 4 | `04_mongo_file.py` | Separate external INI credential files for dev, test and prod |

Stages 2–4 reuse exactly the same MongoDB operation in `mongo_demo.py`: check the server-side environment marker, save a student, and read students. The MySQL example demonstrates the corresponding SQL operation; this lab does not migrate data between database engines.

Every password committed in this starter is deliberately public, disposable classroom data. `prod` is a local simulation with its own container and volume. Use real secret-management infrastructure for real production credentials.

## Start with your own fork

1. Select **Fork** on [WaqasSaleem97/Databases](https://github.com/WaqasSaleem97/Databases).
2. Keep the fork name `Databases` under your own GitHub account.
3. Clone your fork inside the Ubuntu environment prepared in Lab 1:

   ```bash
   cd ~
   git clone git@github.com:<your-username>/Databases.git
   cd Databases
   ```

Replace `<your-username>` with your actual GitHub username. `origin` must point to your fork. Use the `DevOps` repository for the screenshot/PDF submission specified by Lab 4.

## Build and start

Docker Engine and its Compose plugin must already work. See [Docker's Ubuntu installation instructions](https://docs.docker.com/engine/install/ubuntu/) if needed. Run all following commands from your cloned `Databases` directory, using the same terminal session.

```bash
export LAB_UID="$(id -u)"
export LAB_GID="$(id -g)"
docker compose config --quiet
docker compose build app
docker compose up -d --wait mysql mongo-dev mongo-test mongo-prod
docker compose ps
```

The UID/GID settings let the application create local configuration files owned by your Ubuntu account. They are not database credentials. The `app` service has a tools profile and is run on demand; it is not a background web server. Compose supports explicitly targeting such a service. [1]

There are five services: `app`, `mysql`, `mongo-dev`, `mongo-test`, and `mongo-prod`. I recommend about 4 GB RAM available to Docker for the classroom exercise; this is a planning suggestion, not a vendor minimum.

## Endpoints and dummy accounts

| Database | Endpoint FROM the app container | Published host endpoint | Database / auth source | App username | Dummy password |
| --- | --- | --- | --- | --- | --- |
| MySQL | `mysql:3306` | `127.0.0.1:3307` | `school_mysql` | `mysql_student` | `MysqlDemoOnly123!` |
| MongoDB dev | `mongo-dev:27017` | `127.0.0.1:27017` | `school_dev` | `dev_user` | `DevDemoOnly123!` |
| MongoDB test | `mongo-test:27017` | `127.0.0.1:27018` | `school_test` | `test_user` | `TestDemoOnly123!` |
| MongoDB simulated prod | `mongo-prod:27017` | `127.0.0.1:27019` | `school_prod` | `prod_user` | `ProdDemoOnly123!` |

Use the service-name endpoints in the Python container. Its `localhost` refers to the app container itself. For MongoDB, `auth_source` is the database in which the application user was created. [2]

## Stages 1 and 2 — hardcoded settings

```bash
docker compose run --rm app python 01_mysql_hardcoded.py
docker compose run --rm app python 02_mongo_hardcoded.py
```

Each run displays its configuration source, endpoint, database, server-side marker and student records. It never prints the password. The hardcoded settings are intentional counterexamples for teaching.

## Stage 3 — environment variables

The `app.environment` list in `compose.yaml` passes the named variables from your terminal to the application container. Python reads its process environment; the Python script does not automatically load a `.env` file. This pass-through behavior is documented by Docker. [3]

Choose dev and enter the matching dummy password from the table when prompted. `read -s` keeps it out of the terminal output and command history:

```bash
export APP_ENV=dev
export MONGO_HOST=mongo-dev
export MONGO_PORT=27017
export MONGO_DATABASE=school_dev
export MONGO_USERNAME=dev_user
export MONGO_AUTH_SOURCE=school_dev
read -r -s -p "Dev database password: " MONGO_PASSWORD
echo
export MONGO_PASSWORD
docker compose run --rm app python 03_mongo_env.py
```

Choose test:

```bash
export APP_ENV=test
export MONGO_HOST=mongo-test
export MONGO_PORT=27017
export MONGO_DATABASE=school_test
export MONGO_USERNAME=test_user
export MONGO_AUTH_SOURCE=school_test
read -r -s -p "Test database password: " MONGO_PASSWORD
echo
export MONGO_PASSWORD
docker compose run --rm app python 03_mongo_env.py
```

Choose simulated prod:

```bash
export APP_ENV=prod
export MONGO_HOST=mongo-prod
export MONGO_PORT=27017
export MONGO_DATABASE=school_prod
export MONGO_USERNAME=prod_user
export MONGO_AUTH_SOURCE=school_prod
read -r -s -p "Simulated prod database password: " MONGO_PASSWORD
echo
export MONGO_PASSWORD
docker compose run --rm app python 03_mongo_env.py
```

`APP_ENV` is a label and consistency check. Changing only that label does not replace the endpoint or credentials. Supply the complete profile. Missing settings cause an error instead of falling back to another environment.

## Stage 4 — external credential files

```bash
docker compose run --rm app python prepare_config.py
docker compose run --rm app python 04_mongo_file.py --env dev
docker compose run --rm app python 04_mongo_file.py --env test
docker compose run --rm app python 04_mongo_file.py --env prod
```

The preparation command copies `config-examples/*.ini.example` into ignored `config/*.ini` files without overwriting existing files. A bind mount makes those files available inside `/app/config`. File mode selects the named file and ignores shell MongoDB settings. Python uses `ConfigParser(interpolation=None)` so `%` characters in passwords stay literal. INI files are Python's configuration-file choice here; this is not the Java `.properties` parser. [4]

Do not quote an INI password as if it were a shell string. Restrict file access and provide only the selected deployment's credentials in a real system. Environment variables and plaintext files are configuration delivery options, not encryption or a secret-management service. [5]

## Verify

Offline configuration and mocked database-boundary checks:

```bash
docker compose run --rm app python -m unittest discover -s tests -v
```

Live checks after the four databases are healthy and local configs are prepared:

```bash
docker compose run --rm app python smoke_test.py
```

The live smoke test exercises all four stages across all required environments plus wrong-password, missing-password, and marker-mismatch failures: 11 scenarios in total. It expects the original dummy credentials and templates. The workflow under `.github/workflows/verify.yml` performs the same checks on pushes and pull requests to `main`. Forks may require GitHub Actions to be enabled before their workflows run.

## Stop or reset

```bash
docker compose down
```

To erase this Compose project's disposable database volumes and initialize them again:

```bash
docker compose down -v
docker compose up -d --wait mysql mongo-dev mongo-test mongo-prod
```

Initial database users and seed scripts run for an empty data directory. Editing initialization environment variables does not rotate an existing database account's password. Reset only this disposable lab's volumes, or update users explicitly. [6][7]

## Files

- `Dockerfile`, `.dockerignore`, `requirements.txt`: Python runtime image and dependencies.
- `compose.yaml`: app and four database services.
- `01_*` through `04_*`: the four demonstration entry points.
- `settings.py`, `mongo_demo.py`: configuration readers and shared MongoDB operation.
- `db-init/`: database users, student records and environment markers.
- `config-examples/`: public dummy templates; actual config copies stay ignored.
- `tests/`, `smoke_test.py`, `.github/workflows/verify.yml`: offline and live verification.

The evidence rules, exact screenshot names, exam questions and PDF submission requirements are in [Lab 4](https://github.com/WaqasSaleem97/DevOps_F26/blob/main/Labs/Lab04/README.md).

## Official references

1. [Docker Compose profiles](https://docs.docker.com/reference/compose-file/profiles/)
2. [MongoDB: Create a MongoClient](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/mongoclient/)
3. [Docker: Set container environment variables](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/)
4. [Python: configparser](https://docs.python.org/3/library/configparser.html)
5. [OWASP: Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
6. [Docker Official Image: MongoDB](https://github.com/docker-library/docs/blob/master/mongo/README.md)
7. [Docker Official Image: MySQL](https://github.com/docker-library/docs/blob/master/mysql/README.md)
8. [MySQL Connector/Python: Connecting](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html)
