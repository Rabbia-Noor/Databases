"""STAGE 3: One unchanged program; deployment variables select the database."""

import sys

from mongo_demo import run_demo
from settings import LabError, load_environment


def main() -> int:
    try:
        settings = load_environment()
        run_demo(settings, source="process environment variables")
        return 0
    except LabError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
