# Validation Record

[GitHub Actions run 39257976455](https://github.com/WaqasSaleem97/Databases/actions/runs/39257976455) passed on 19 October 2026 for source commit `7c46fbb5fa21ab52254d1bbcd73d2a3eed59457f`.

## What Was Verified

Python 3.12 ran directly on the Ubuntu runner host. Docker Compose ran only MySQL and the three MongoDB services.

- Both Python database drivers installed successfully.
- The database-only Compose configuration passed validation, and all four services became healthy.
- All eight successful connection combinations passed: MySQL, hardcoded MongoDB, three environment-variable profiles and three credential-file sections.
- Missing environment-variable rejection and wrong file-password rejection passed.
- The file version selected the default dev section despite prod URI exports.
- All 11 live scenarios passed.
- The same MongoDB connection block was used across stages 2–4.
- Disposable database services and volumes were removed after verification.

## Documentation Checks

- Both guides contain the same four short examples, each 12–17 lines.
- Students edit only `db_connect.py` and create one local `credentials.ini` copy.
- The supplied Ubuntu Docker installation commands and host Python setup are preserved.
- Python and Bash syntax, navigation links and all three INI sections were checked.
- Lab 4 has nine task screenshot lists and 29 mandatory filenames synchronized with `evidence.json`.
- The old multi-file application, helper modules and unrelated student tests were removed.

The workflow runs `python tests/verify_connections.py` against the README examples. This is instructor verification; the student's repeated run command is `python db_connect.py`.
