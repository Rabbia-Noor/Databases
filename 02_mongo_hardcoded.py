"""STAGE 2: Hardcoded MongoDB settings; use dummy credentials only."""

import sys

from mongo_demo import run_demo
from settings import LabError, MongoSettings


def main() -> int:
    settings = MongoSettings(
        environment="dev",
        host="127.0.0.1",
        port=27017,
        database="school_dev",
        username="dev_user",
        password="DevDemoOnly123!",
        auth_source="school_dev",
    )
    try:
        run_demo(settings, source="hardcoded Python values")
        return 0
    except LabError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
