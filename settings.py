"""Read connection settings; never embed deployment credentials here."""

import configparser
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping


class LabError(Exception):
    """A short, safe-to-display lab error."""


@dataclass(frozen=True)
class MongoSettings:
    environment: str
    host: str
    port: int
    database: str
    username: str
    password: str = field(repr=False)
    auth_source: str


def make_settings(environment: str, values: Mapping[str, str]) -> MongoSettings:
    if environment not in {"dev", "test", "prod"}:
        raise LabError("APP_ENV must be dev, test, or prod; no default is selected.")
    keys = ("host", "port", "database", "username", "password", "auth_source")
    missing = [key for key in keys if not values.get(key, "").strip()]
    if missing:
        raise LabError("Missing MongoDB settings: " + ", ".join(missing))
    try:
        port = int(values["port"])
    except (ValueError, TypeError):
        raise LabError("MongoDB port must be an integer.") from None
    if not 1 <= port <= 65535:
        raise LabError("MongoDB port must be between 1 and 65535.")
    return MongoSettings(
        environment=environment,
        host=values["host"].strip(),
        port=port,
        database=values["database"].strip(),
        username=values["username"].strip(),
        password=values["password"],  # Preserve special characters verbatim.
        auth_source=values["auth_source"].strip(),
    )


def load_environment() -> MongoSettings:
    """Read only this process's variables; do not automatically load a .env file."""
    return make_settings(
        os.environ.get("APP_ENV", ""),
        {
            "host": os.environ.get("MONGO_HOST", ""),
            "port": os.environ.get("MONGO_PORT", ""),
            "database": os.environ.get("MONGO_DATABASE", ""),
            "username": os.environ.get("MONGO_USERNAME", ""),
            "password": os.environ.get("MONGO_PASSWORD", ""),
            "auth_source": os.environ.get("MONGO_AUTH_SOURCE", ""),
        },
    )


def load_file(environment: str, config_dir: Path) -> MongoSettings:
    if environment not in {"dev", "test", "prod"}:
        raise LabError("Select dev, test, or prod; no default is selected.")
    path = config_dir / f"{environment}.ini"
    parser = configparser.ConfigParser(interpolation=None)
    try:
        with path.open(encoding="utf-8") as stream:
            parser.read_file(stream)
    except OSError:
        raise LabError("Configuration file is missing or unreadable; run prepare_config.py.") from None
    except configparser.Error:
        # Parser errors can include whole credential lines; do not echo them.
        raise LabError("Invalid INI configuration; check its sections and keys.") from None
    if not parser.has_section("application") or not parser.has_section("mongodb"):
        raise LabError("The file needs [application] and [mongodb] sections.")
    if parser["application"].get("environment", "") != environment:
        raise LabError("The selected environment does not match the configuration file.")
    return make_settings(environment, parser["mongodb"])
