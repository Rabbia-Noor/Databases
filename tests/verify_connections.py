"""Instructor check: run the README examples against the four live databases."""

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text()
STAGES = dict(re.findall(
    r"<!-- stage: ([a-z_]+) -->\n```python\n(.*?)```",
    README,
    flags=re.DOTALL,
))
EXPECTED_STAGES = {"mysql", "mongo_hardcoded", "mongo_env", "mongo_file"}
if set(STAGES) != EXPECTED_STAGES:
    raise SystemExit("The four marked README examples are required.")

for name, code in STAGES.items():
    compile(code, name, "exec")
compile((ROOT / "db_connect.py").read_text(), "db_connect.py", "exec")

# The student's MongoDB request and output block must stay the same.
connection_blocks = {
    code[code.index("client = MongoClient"):]
    for name, code in STAGES.items()
    if name.startswith("mongo_")
}
if len(connection_blocks) != 1:
    raise SystemExit("The MongoDB connection blocks differ.")

PROFILES = {
    "dev": ("dev_user", "DevDemoOnly123!", 27017),
    "test": ("test_user", "TestDemoOnly123!", 27018),
    "prod": ("prod_user", "ProdDemoOnly123!", 27019),
}
base_env = {
    key: value for key, value in os.environ.items()
    if not key.startswith("MONGO_") and key != "APP_ENV"
}
passed = 0


def profile(name):
    username, password, port = PROFILES[name]
    return {
        "MONGO_USERNAME": username,
        "MONGO_PASSWORD": password,
        "MONGO_ENDPOINT": f"127.0.0.1:{port}",
        "MONGO_DATABASE": f"school_{name}",
    }


def run(stage, label, target, values=None, failure=None):
    global passed
    (work / "db_connect.py").write_text(STAGES[stage])
    result = subprocess.run(
        [sys.executable, "db_connect.py"],
        cwd=work,
        env={**base_env, **(values or {})},
        text=True,
        capture_output=True,
        timeout=30,
    )
    output = result.stdout + result.stderr
    if failure is None:
        expected_database = "school_mysql" if stage == "mysql" else f"school_{target}"
        expected_port = 3307 if stage == "mysql" else PROFILES[target][2]
        if result.returncode != 0:
            raise RuntimeError(f"{label}: database connection failed.\n{output}")
        for expected in (expected_database, str(expected_port), f"Environment: {target}"):
            if expected not in output:
                raise RuntimeError(f"{label}: missing expected result {expected!r}.\n{output}")
    elif result.returncode == 0 or failure.lower() not in output.lower():
        raise RuntimeError(f"{label}: expected rejection did not occur.\n{output}")
    passed += 1
    print(f"PASS {passed}: {label}", flush=True)


with tempfile.TemporaryDirectory(prefix="lab04-connections-") as directory:
    work = Path(directory)
    (work / "credentials.ini").write_text(
        (ROOT / "credentials.ini.example").read_text()
    )
    (work / "credentials.ini").chmod(0o600)

    run("mysql", "MySQL hardcoded", "dev")
    run("mongo_hardcoded", "MongoDB hardcoded", "dev")

    for name in PROFILES:
        run("mongo_env", f"Environment variables: {name}", name, profile(name))

    for name in PROFILES:
        run("mongo_file", f"Credentials file: {name}", name, {"APP_ENV": name})

    missing = profile("prod")
    del missing["MONGO_DATABASE"]
    run(
        "mongo_env", "Missing variable rejected", "prod", missing,
        failure="Set all four MongoDB environment variables first.",
    )

    credential_path = work / "credentials.ini"
    valid_credentials = credential_path.read_text()
    credential_path.write_text(valid_credentials.replace("TestDemoOnly123!", "wrong"))
    run(
        "mongo_file", "Wrong file password rejected", "test",
        {"APP_ENV": "test"}, failure="Authentication failed",
    )
    credential_path.write_text(valid_credentials)

    # An unset APP_ENV defaults to the dev file section, even with prod connection variables.
    run(
        "mongo_file", "Default dev section ignores prod connection variables",
        "dev", profile("prod"),
    )

print(f"All {passed} live scenarios passed.", flush=True)
