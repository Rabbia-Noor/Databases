"""Optional live check: run only after docker compose up -d --wait."""

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run_case(label, script, *, environment=None, arguments=(), expect_success=True, expected_text="PASS:"):
    result = subprocess.run(
        [sys.executable, str(ROOT / script), *arguments],
        cwd=ROOT,
        env=environment if environment is not None else os.environ.copy(),
        capture_output=True,
        text=True,
        timeout=30,
    )
    success = result.returncode == 0
    matched = success == expect_success and expected_text in result.stdout + result.stderr
    print(f"{'PASS' if matched else 'FAIL'}: {label}")
    if not matched:
        # Application messages exclude credentials; never dump the child environment.
        print(result.stdout + result.stderr)
        raise SystemExit(1)


def main():
    run_case("stage 1: hardcoded MySQL", "01_mysql_hardcoded.py")
    run_case("stage 2: hardcoded MongoDB", "02_mongo_hardcoded.py")
    profiles = (("dev", "27017", "Dev"), ("test", "27018", "Test"), ("prod", "27019", "Prod"))
    for name, port, prefix in profiles:
        environment = os.environ.copy()
        environment.update(
            APP_ENV=name,
            MONGO_HOST="127.0.0.1",
            MONGO_PORT=port,
            MONGO_DATABASE=f"school_{name}",
            MONGO_USERNAME=f"{name}_user",
            MONGO_PASSWORD=f"{prefix}DemoOnly123!",
            MONGO_AUTH_SOURCE=f"school_{name}",
        )
        run_case(f"stage 3: environment variables -> {name}", "03_mongo_env.py", environment=environment, expected_text=f"marker: {name}")
        run_case(f"stage 4: credential file -> {name}", "04_mongo_file.py", arguments=("--env", name), expected_text=f"marker: {name}")

    wrong_password = environment.copy()
    wrong_password["MONGO_PASSWORD"] = "IntentionallyWrongForLab"
    run_case("wrong password is rejected", "03_mongo_env.py", environment=wrong_password, expect_success=False, expected_text="Authentication failed")
    missing_password = environment.copy()
    missing_password.pop("MONGO_PASSWORD")
    run_case("missing password is rejected without fallback", "03_mongo_env.py", environment=missing_password, expect_success=False, expected_text="Missing MongoDB settings")
    wrong_label = environment.copy()
    wrong_label["APP_ENV"] = "dev"
    run_case("wrong environment marker blocks writes", "03_mongo_env.py", environment=wrong_label, expect_success=False, expected_text="no student was written")
    print("All 11 live scenarios passed.")


if __name__ == "__main__":
    main()
