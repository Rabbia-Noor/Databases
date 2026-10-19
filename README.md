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

The supplied `db_connect.py` starts with this short MySQL connection:

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

`user` and `password` supply the database credentials. `host` identifies the server, `port` identifies its MySQL service, and `database` selects the database. `mysql.connector.connect()` opens the connection. The small query reads an environment value stored in MySQL, so students can see that a database answered.

Run `python db_connect.py`. Expect `Connected to MySQL: school_mysql` and `Environment: dev`.

## Step 2: MongoDB with Values in the Code

Replace the contents of **the same `db_connect.py`** with:

<!-- stage: mongo_hardcoded -->
```python
from pymongo import MongoClient

username = "dev_user"
password = "DevDemoOnly123!"
endpoint = "127.0.0.1:27017"
database_name = "school_dev"

uri = "mongodb://" + username + ":" + password + "@" + endpoint + "/" + database_name

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
database = client[database_name]
database.command("ping")
print("Connected to MongoDB:", database.name)
print("Server:", client.address)
print("Environment:", database.environment_info.find_one()["name"])
client.close()
```

`username`, `password`, `endpoint` and `database_name` hold the connection settings. The `+` operator joins them into `uri`.

`MongoClient(uri)` creates the client, and `client[database_name]` selects the database. The URI's database is also the authentication database in this lab.

`database.command("ping")` sends a real request. Creating a client or selecting a database by itself does not prove that a server is reachable. The environment value is read from the selected database. The `5000` option limits server selection to five seconds.

Run `python db_connect.py`. Expect `school_dev`, port `27017` and environment `dev`.

## Step 3: Read Environment Variables with os.getenv()

Replace the same file with:

<!-- stage: mongo_env -->
```python
import os
from pymongo import MongoClient

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
endpoint = os.getenv("MONGO_ENDPOINT")
database_name = os.getenv("MONGO_DATABASE")

if not username or not password or not endpoint or not database_name:
    raise SystemExit("Set all four MongoDB environment variables first.")

uri = "mongodb://" + username + ":" + password + "@" + endpoint + "/" + database_name

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
database = client[database_name]
database.command("ping")
print("Connected to MongoDB:", database.name)
print("Server:", client.address)
print("Environment:", database.environment_info.find_one()["name"])
client.close()
```

The four settings are read separately with `os.getenv()`. Python then builds `uri` with the same concatenation line used in Step 2. The MongoDB connection and output lines stay the same. The short check stops the program if a required variable is missing.

Use one complete profile at a time in the same Ubuntu shell. These commands contain **public dummy credentials**. `clear` removes them from the visible terminal before you capture the connection result. Do not print `MONGO_PASSWORD`, the assembled URI or include the exports in screenshots.

### Dev

```bash
export MONGO_USERNAME=dev_user
export MONGO_PASSWORD='DevDemoOnly123!'
export MONGO_ENDPOINT=127.0.0.1:27017
export MONGO_DATABASE=school_dev
clear
python db_connect.py
```

### Test

```bash
export MONGO_USERNAME=test_user
export MONGO_PASSWORD='TestDemoOnly123!'
export MONGO_ENDPOINT=127.0.0.1:27018
export MONGO_DATABASE=school_test
clear
python db_connect.py
```

### Simulated Prod

```bash
export MONGO_USERNAME=prod_user
export MONGO_PASSWORD='ProdDemoOnly123!'
export MONGO_ENDPOINT=127.0.0.1:27019
export MONGO_DATABASE=school_prod
clear
python db_connect.py
```

`os.getenv()` reads the environment of the Python process. Set all four variables for each profile; Python reads them again on each run. Changing `APP_ENV` alone has no effect in this version because the code does not read it.

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
username = dev_user
password = DevDemoOnly123!
endpoint = 127.0.0.1:27017
database = school_dev

[test]
username = test_user
password = TestDemoOnly123!
endpoint = 127.0.0.1:27018
database = school_test

[prod]
username = prod_user
password = ProdDemoOnly123!
endpoint = 127.0.0.1:27019
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
username = config[environment]["username"]
password = config[environment]["password"]
endpoint = config[environment]["endpoint"]
database_name = config[environment]["database"]

uri = "mongodb://" + username + ":" + password + "@" + endpoint + "/" + database_name

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
database = client[database_name]
database.command("ping")
print("Connected to MongoDB:", database.name)
print("Server:", client.address)
print("Environment:", database.environment_info.find_one()["name"])
client.close()
```

`config.read()` loads the INI file, and `config[environment]` chooses its section. `APP_ENV` selects `dev`, `test` or `prod`; if it is unset, the default is `dev`. The username, password, endpoint and database name come from that section. Python builds `uri` using the same concatenation line as before. The MongoDB connection and output lines remain unchanged.

```bash
export APP_ENV=dev
python db_connect.py

export APP_ENV=test
python db_connect.py

export APP_ENV=prod
python db_connect.py
```

This version reads its connection settings from the selected INI section. `interpolation=None` makes the file reader treat values literally. The supplied dummy credentials are joined directly into the URI.

Keep `credentials.ini` local. It is ignored by Git; the example contains public dummy values. Mode `600` restricts the local file to its owner, and an INI file stores plaintext.

## What Students Change

| Stage | Change in `db_connect.py` | How to choose the target |
| --- | --- | --- |
| 1. MySQL | Start with the supplied MySQL connection | Values in the code |
| 2. MongoDB | Replace MySQL with the short MongoDB example | Values in the code |
| 3. Environment | Add `import os`; read four separate values with `os.getenv()` | Export username, password, endpoint and database |
| 4. File | Read the same four values with `configparser` | Export `APP_ENV` to select an INI section |

Follow the screenshot and submission requirements in [DevOps Lab 4](https://github.com/WaqasSaleem97/DevOps_F26/tree/main/Labs/Lab04).

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
