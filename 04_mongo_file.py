"""STAGE 4: One unchanged program; choose one external INI credential file."""

import argparse
import sys
from pathlib import Path

from mongo_demo import run_demo
from settings import LabError, load_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", required=True, choices=("dev", "test", "prod"))
    parser.add_argument("--config-dir", type=Path, default=Path(__file__).resolve().parent / "config")
    args = parser.parse_args()
    try:
        settings = load_file(args.env, args.config_dir)
        run_demo(settings, source=f"external INI file ({args.env}.ini)")
        return 0
    except LabError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
