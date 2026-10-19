# Databases — Python on Ubuntu with Docker databases

Fork this repository to complete [DevOps Lab 4](https://github.com/WaqasSaleem97/DevOps_F26/tree/main/Labs/Lab04). Write, edit and run the Python code directly on the Ubuntu host. Docker Compose runs MySQL and three MongoDB databases.

| Stage | Python program | Connection settings |
| --- | --- | --- |
| 1 | `01_mysql_hardcoded.py` | Hardcoded MySQL endpoint, username and password |
| 2 | `02_mongo_hardcoded.py` | Hardcoded MongoDB endpoint, username and password |
| 3 | `03_mongo_env.py` | Host process environment variables for dev, test and prod |
| 4 | `04_mongo_file.py` | External host credential files for dev, test and prod |

Stages 2–4 reuse the same MongoDB operation in `mongo_demo.py`: check a marker stored in the selected database, save a student, and read students. Every successful run shows the actual endpoint, database name and environment marker. Passwords are not printed.

All committed credentials are disposable classroom examples. `prod` is a local simulation with a separate database container and data volume.

## Start with your own fork

1. Select **Fork** on [WaqasSaleem97/Databases](https://github.com/WaqasSaleem97/Databases).
2. Keep the name `Databases` under your own GitHub account.
3. Clone your fork on the Ubuntu host:

   ```bash
   cd ~
   git clone git@github.com:<your-username>/Databases.git
   cd Databases
   ```

Replace `<your-username>` with your actual GitHub username. Submit the evidence and solution PDF to your separate `DevOps` repository as specified in Lab 4.

## Install Docker, Docker Compose and Python on Ubuntu

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 python3 python3-venv python3-pip
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
```

## Prepare the host Python environment

Run these commands from your `Databases` clone:

```bash
cd ~/Databases
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Keep this virtual environment active for every `python` command below. After opening a new terminal, return to `~/Databases` and run `source .venv/bin/activate` again. Edit the `.py` files directly in this directory using your editor.

## Start the databases

```bash
docker compose up -d --wait mysql mongo-dev mongo-test mongo-prod
docker compose ps
```

Compose defines exactly four services. Each database publishes a port on the Ubuntu host's loopback interface, which is the endpoint used by Python:

| Database | Endpoint used by host Python | Database / MongoDB auth source | Username | Dummy password |
| --- | --- | --- | --- | --- |
| MySQL | `127.0.0.1:3307` | `school_mysql` | `mysql_student` | `MysqlDemoOnly123!` |
| MongoDB dev | `127.0.0.1:27017` | `school_dev` | `dev_user` | `DevDemoOnly123!` |
| MongoDB test | `127.0.0.1:27018` | `school_test` | `test_user` | `TestDemoOnly123!` |
| MongoDB simulated prod | `127.0.0.1:27019` | `school_prod` | `prod_user` | `ProdDemoOnly123!` |

Run Python on the same Ubuntu machine as these published ports. MongoDB users are created inside their corresponding data database, so each profile's `auth_source` matches that database.

## Stages 1 and 2 — hardcoded connections

```bash
python 01_mysql_hardcoded.py
python 02_mongo_hardcoded.py
```

The first script shows the MySQL connection and the second shows the MongoDB dev connection. The connection settings in these two files are intentionally hardcoded for the demonstration.

## Stage 3 — environment variables on the host

The script reads the current Python process environment through `os.environ`. It does not automatically load a `.env` file.

Select dev, entering its dummy password from the table at the hidden prompt:

```bash
export APP_ENV=dev
export MONGO_HOST=127.0.0.1
export MONGO_PORT=27017
export MONGO_DATABASE=school_dev
export MONGO_USERNAME=dev_user
export MONGO_AUTH_SOURCE=school_dev
read -r -s -p "Dev database password: " MONGO_PASSWORD
echo
export MONGO_PASSWORD
python 03_mongo_env.py
```

Select test:

```bash
export APP_ENV=test
export MONGO_HOST=127.0.0.1
export MONGO_PORT=27018
export MONGO_DATABASE=school_test
export MONGO_USERNAME=test_user
export MONGO_AUTH_SOURCE=school_test
read -r -s -p "Test database password: " MONGO_PASSWORD
echo
export MONGO_PASSWORD
python 03_mongo_env.py
```

Select simulated prod:

```bash
export APP_ENV=prod
export MONGO_HOST=127.0.0.1
export MONGO_PORT=27019
export MONGO_DATABASE=school_prod
export MONGO_USERNAME=prod_user
export MONGO_AUTH_SOURCE=school_prod
read -r -s -p "Simulated prod database password: " MONGO_PASSWORD
echo
export MONGO_PASSWORD
python 03_mongo_env.py
```

Supply the complete matching profile. `APP_ENV` is a label and consistency check; changing it alone does not select different credentials. Missing values cause an error instead of a fallback to another environment.

A successful test run includes the following connection details:

```text
Configuration source: process environment variables
Connected to: test | 127.0.0.1:27018
Database: school_test | marker: test
```

The student records and PASS message follow. The marker is read from MongoDB itself.

## Stage 4 — external credential files on the host

```bash
python prepare_config.py
python 04_mongo_file.py --env dev
python 04_mongo_file.py --env test
python 04_mongo_file.py --env prod
```

The preparation command copies the supplied dummy templates into `config/dev.ini`, `config/test.ini` and `config/prod.ini`, preserving any existing files. Edit those files directly on the host when demonstrating external configuration. Generated credential files remain ignored by Git.

File mode reads the selected file and ignores MongoDB variables left in the terminal. Python's `ConfigParser(interpolation=None)` keeps `%` characters literal. These INI files are plaintext, so externalizing configuration does not encrypt a password or replace a production secret-management service.

## Verify the connections

Run the offline checks and then the live checks from the active host virtual environment:

```bash
python -m unittest discover -s tests -v
python smoke_test.py
```

The live smoke test checks MySQL, hardcoded MongoDB, all three environment-variable profiles, all three credential files, and three expected failure cases: 11 scenarios in total. It expects the original dummy accounts and templates. The GitHub Actions workflow runs Python directly on its host runner against the four Docker database services as well.

## Stop or reset the databases

```bash
docker compose down
```

To erase this Compose project's disposable data volumes and initialize fresh data:

```bash
docker compose down -v
docker compose up -d --wait mysql mongo-dev mongo-test mongo-prod
```

Initialization scripts run for an empty database data directory. Editing initialization variables does not rotate an account already stored in an existing volume.

## Files

- `compose.yaml`: MySQL and the three MongoDB database services.
- `requirements.txt`: drivers installed in the host Python virtual environment.
- `01_*` through `04_*`: Python entry points run directly on Ubuntu.
- `settings.py`, `mongo_demo.py`: configuration readers and the shared MongoDB operation.
- `db-init/`: database users, markers and seed student records.
- `config-examples/`: public dummy templates; editable copies stay local under `config/`.
- `tests/`, `smoke_test.py`, `.github/workflows/verify.yml`: offline and live verification.

Find the exact screenshot names, exam questions and submission requirements in [Lab 4](https://github.com/WaqasSaleem97/DevOps_F26/blob/main/Labs/Lab04/README.md).

## Official references

- [Ubuntu: docker.io](https://packages.ubuntu.com/noble/docker.io)
- [Ubuntu: Docker Compose v2](https://packages.ubuntu.com/noble/docker-compose-v2)
- [Docker: Linux post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/)
- [Python: virtual environments](https://docs.python.org/3/library/venv.html)
- [Python: os.environ](https://docs.python.org/3/library/os.html#os.environ)
- [MySQL Connector/Python: Connecting](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html)
- [MongoDB: Create a MongoClient](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/mongoclient/)
- [Python: configparser](https://docs.python.org/3/library/configparser.html)
- [OWASP: Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
