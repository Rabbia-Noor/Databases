# Python Database Connections — Lab 4

Fork this repository and work in your fork on Ubuntu. **Edit only `db_connect.py`**, replacing its contents at each step. Run the same command every time:

```bash
python db_connect.py
```

Python runs directly on Ubuntu. Docker Compose runs MySQL and three separate MongoDB databases. The supplied accounts are public dummy classroom accounts; `prod` is a local simulation.

The full tasks, screenshot filenames and submission requirements are in [DevOps Lab 4](https://github.com/WaqasSaleem97/DevOps_F26/tree/main/Labs/Lab04).

## Install Docker and Docker Compose on Ubuntu

1. Connect to your assigned Ubuntu server.

2. Update the Ubuntu package index and install Docker Engine and `curl`. On Ubuntu, the required package name is `docker.io`:

   ```bash
   sudo apt update -y
   sudo apt install -y docker.io curl
   ```

3. Create the system-wide Docker CLI plug-in directory and download the Docker Compose plug-in for an `x86_64` Ubuntu server:

   ```bash
   sudo mkdir -p /usr/local/lib/docker/cli-plugins
   sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
   sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
   ```

4. Start the Docker service and add your current Ubuntu account to the `docker` group:

   ```bash
   sudo systemctl start docker
   sudo usermod -aG docker $USER
   exit
   ```

   Completely sign out of the Ubuntu server and reconnect so that the new group membership takes effect. Opening only a new terminal tab is not sufficient.

5. Reconnect and verify the Git, Docker, and Docker Compose installations:

   ```bash
   ssh <github-username>@<ubuntu-server-ip>
   git --version
   docker --version
   docker compose version
   ```

   Do not continue until all three version commands display their installed versions.

   - Save a screenshot showing the three commands and their installed versions as `docker_installation.png`.

## Install Python on Ubuntu

```bash
sudo apt install -y python3 python3-venv python3-pip
cd ~/Databases
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Use your editor to change `db_connect.py`. Run Python from `~/Databases` with `.venv` active. Activate it again after reconnecting.

## Start the Databases

```bash
docker compose up -d --wait mysql mongo-dev mongo-test mongo-prod
docker compose ps
```

| Database | Host endpoint | Database name | Dummy username | Dummy password |
| --- | --- | --- | --- | --- |
| MySQL | `127.0.0.1:3307` | `school_mysql` | `mysql_student` | `MysqlDemoOnly123!` |
| MongoDB dev | `127.0.0.1:27017` | `school_dev` | `dev_user` | `DevDemoOnly123!` |
| MongoDB test | `127.0.0.1:27018` | `school_test` | `test_user` | `TestDemoOnly123!` |
| MongoDB simulated prod | `127.0.0.1:27019` | `school_prod` | `prod_user` | `ProdDemoOnly123!` |

## Step 1: MySQL with Values in the Code

The supplied `db_connect.py` starts with this code. It is the Python equivalent of setting a MySQL username, password and JDBC endpoint:

<!-- stage: mysql -->
```python
import mysql.connector

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="mysql_student",
    password="MysqlDemoOnly123!",
    database="school_mysql",
)

print("Connected to MySQL:", connection.database)
print("Server:", connection.server_host, connection.server_port)
cursor = connection.cursor()
cursor.execute("SELECT environment FROM environment_info")
print("Environment:", cursor.fetchone()[0])
cursor.close()
connection.close()
```

The host, port and database name correspond to the parts of `jdbc:mysql://host:port/database`. `mysql.connector.connect()` opens the connection. The small query reads an environment value already stored in MySQL, so students can see that a database answered.

Run `python db_connect.py`. Expect `Connected to MySQL: school_mysql` and `Environment: dev`.

## Step 2: MongoDB with Values in the Code

Replace the contents of **the same `db_connect.py`** with:

<!-- stage: mongo_hardcoded -->
```python
from pymongo import MongoClient

uri = "mongodb://dev_user:DevDemoOnly123!@127.0.0.1:27017/school_dev"
database_name = "school_dev"

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
database = client[database_name]
database.command("ping")
print("Connected to MongoDB:", database.name)
print("Server:", client.address)
print("Environment:", database.environment_info.find_one()["name"])
client.close()
```

`MongoClient(uri)` corresponds to the Java MongoDB client, and `client[database_name]` corresponds to selecting a database with `getDB(...)`. The URI contains the username, password, endpoint and authentication database. The selected database matches that authentication database in this lab.

`database.command("ping")` sends a real request. Creating a client or selecting a database by itself does not prove that a server is reachable. The environment value is read from the selected database. The `5000` option limits server selection to five seconds.

Run `python db_connect.py`. Expect `school_dev`, port `27017` and environment `dev`.

## Step 3: Read Environment Variables with os.getenv()

Replace the same file with:

<!-- stage: mongo_env -->
```python
import os
from pymongo import MongoClient

uri = os.getenv("MONGO_URI")
database_name = os.getenv("MONGO_DATABASE")

if not uri or not database_name:
    raise SystemExit("Set MONGO_URI and MONGO_DATABASE first.")

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
database = client[database_name]
database.command("ping")
print("Connected to MongoDB:", database.name)
print("Server:", client.address)
print("Environment:", database.environment_info.find_one()["name"])
client.close()
```

Only the source of `uri` and `database_name` changes. The MongoDB connection and output lines stay the same. The two-line check explains missing variables rather than allowing a default connection.

Use one complete profile at a time in the same Ubuntu shell. These commands contain **public dummy credentials**. `clear` removes them from the visible terminal before you capture the connection result. Do not print `MONGO_URI` or include the exports in screenshots.

### Dev

```bash
export MONGO_URI='mongodb://dev_user:DevDemoOnly123!@127.0.0.1:27017/school_dev'
export MONGO_DATABASE=school_dev
clear
python db_connect.py
```

### Test

```bash
export MONGO_URI='mongodb://test_user:TestDemoOnly123!@127.0.0.1:27018/school_test'
export MONGO_DATABASE=school_test
clear
python db_connect.py
```

### Simulated Prod

```bash
export MONGO_URI='mongodb://prod_user:ProdDemoOnly123!@127.0.0.1:27019/school_prod'
export MONGO_DATABASE=school_prod
clear
python db_connect.py
```

`os.getenv()` reads the environment of the Python process. Both exports change between profiles; Python reads them again on each run. Changing `APP_ENV` alone has no effect in this version because the code does not read it.

## Step 4: Read a Credentials File

Create one local credential file from the supplied example:

```bash
cp -n credentials.ini.example credentials.ini
chmod 600 credentials.ini
```

It contains three sections:

```ini
# Public dummy values for the disposable classroom databases only.
[dev]
uri = mongodb://dev_user:DevDemoOnly123!@127.0.0.1:27017/school_dev
database = school_dev

[test]
uri = mongodb://test_user:TestDemoOnly123!@127.0.0.1:27018/school_test
database = school_test

[prod]
uri = mongodb://prod_user:ProdDemoOnly123!@127.0.0.1:27019/school_prod
database = school_prod
```

Replace the contents of the same `db_connect.py` with:

<!-- stage: mongo_file -->
```python
import os
import configparser
from pymongo import MongoClient

config = configparser.ConfigParser(interpolation=None)
config.read("credentials.ini")
environment = os.getenv("APP_ENV", "dev")
uri = config[environment]["uri"]
database_name = config[environment]["database"]

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
database = client[database_name]
database.command("ping")
print("Connected to MongoDB:", database.name)
print("Server:", client.address)
print("Environment:", database.environment_info.find_one()["name"])
client.close()
```

`config.read()` loads the INI file, and `config[environment]` chooses its section. `APP_ENV` selects `dev`, `test` or `prod`; if it is unset, the default is `dev`. The URI and database name come from that section. The MongoDB connection and output lines remain unchanged.

```bash
export APP_ENV=dev
python db_connect.py

export APP_ENV=test
python db_connect.py

export APP_ENV=prod
python db_connect.py
```

This version does not read `MONGO_URI` or `MONGO_DATABASE`. `interpolation=None` lets a literal `%` in the file remain a literal character; credentials inside a URI still require correct URI encoding.

Keep `credentials.ini` local. It is ignored by Git; the example contains public dummy values. Mode `600` restricts the local file to its owner, and an INI file stores plaintext.

## What Students Change

| Stage | Change in `db_connect.py` | How to choose the target |
| --- | --- | --- |
| 1. MySQL | Start with the supplied MySQL connection | Values in the code |
| 2. MongoDB | Replace MySQL with the short MongoDB example | Values in the code |
| 3. Environment | Add `import os`; load two values with `os.getenv()` | Export `MONGO_URI` and `MONGO_DATABASE` |
| 4. File | Load the same two values with `configparser` | Export `APP_ENV` to select an INI section |

Commit the completed `db_connect.py` to your fork. Submit your screenshots, answers and `Lab4_Solution.pdf` to your `DevOps/Labs/Lab04` directory as described in the course lab.

## Stop the Databases

```bash
docker compose down
```

Initialization scripts create the dummy accounts and environment markers on the first start of empty volumes. To intentionally reset this disposable lab, `docker compose down -v` also deletes its database data.

## Instructor Verification

The automated workflow runs the four examples above directly on the runner host against the database containers. It tests MySQL, hardcoded MongoDB, all three environment profiles and all three INI sections, plus missing-variable and rejected-password cases. These verification files are not part of the student's editing task.

See [VALIDATION.md](VALIDATION.md) for the verification status.

## Official References

- [MySQL Connector/Python: Connecting to MySQL](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html)
- [MongoDB: Connect to MongoDB with PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/)
- [Python: os.getenv](https://docs.python.org/3/library/os.html#os.getenv)
- [Python: configparser](https://docs.python.org/3/library/configparser.html)
- [Python: virtual environments](https://docs.python.org/3/library/venv.html)
- [Docker: Install the Compose plugin manually](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually)
- [Docker: Linux post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/)
- [Git: gitignore](https://git-scm.com/docs/gitignore)
