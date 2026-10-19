"""The SAME database operation is reused in stages 2, 3 and 4."""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError

from settings import LabError, MongoSettings


def run_demo(settings: MongoSettings, source: str) -> None:
    try:
        # Separate keyword arguments keep special characters in passwords literal.
        with MongoClient(
            host=settings.host,
            port=settings.port,
            username=settings.username,
            password=settings.password,
            authSource=settings.auth_source,
            directConnection=True,
            serverSelectionTimeoutMS=3000,
            connectTimeoutMS=3000,
            socketTimeoutMS=3000,
            appname="classroom-credential-lab",
        ) as client:
            client.admin.command("ping")
            database = client[settings.database]
            marker = database.environment_info.find_one({"_id": "environment"})
            if marker is None or marker.get("name") != settings.environment:
                raise LabError("Database marker does not match the selected environment; no student was written.")

            # Only write AFTER reading the server-side marker.
            database.students.update_one(
                {"roll_no": "DEMO-001"},
                {"$set": {"name": "Ali", "environment": settings.environment}},
                upsert=True,
            )
            print(f"Configuration source: {source}")
            print(f"Connected to: {settings.environment} | {settings.host}:{settings.port}")
            print(f"Database: {settings.database} | marker: {marker['name']}")
            for student in database.students.find({}, {"_id": 0}).sort("roll_no", 1):
                print(f"Student: {student['roll_no']} | {student['name']}")
            print("PASS: student saved and read from the selected database.")
    except OperationFailure as error:
        if error.code == 18:
            raise LabError("Authentication failed; check username, password, and auth source.") from None
        if error.code == 13:
            raise LabError("Authorization failed; check this user's database permissions.") from None
        raise LabError("MongoDB rejected the operation; check database setup.") from None
    except ConnectionFailure:
        raise LabError("Cannot reach MongoDB; check the endpoint and container health.") from None
    except PyMongoError:
        raise LabError("MongoDB connection settings or operation are invalid.") from None
