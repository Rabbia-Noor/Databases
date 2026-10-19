# Validation Record

[GitHub Actions run 39263060138](https://github.com/WaqasSaleem97/Databases/actions/runs/39263060138) passed on 19 October 2026 for source commit `fff89f05bbd94bf572eac976cedb5ccfe409fd56`.

## Verified Behavior

Python 3.12 ran directly on the Ubuntu runner host. Docker Compose ran MySQL and the three MongoDB database services.

- Both Python drivers installed, the Compose configuration was valid, and all four databases became healthy.
- All eight successful connections passed: MySQL, hardcoded MongoDB, three environment-variable profiles and three INI sections.
- The MongoDB username, password, endpoint and database were read as separate settings.
- Each MongoDB example built `uri` using quoted strings and the `+` operator with the supplied dummy credentials.
- Missing-variable rejection, wrong file-password rejection and default file-section selection passed.
- All 11 live scenarios passed.
- Disposable database services and volumes were removed.

## Documentation Checks

- Both guides contain the same four Python examples and the same MongoDB connection block.
- Python and Bash syntax, navigation links and valid URIs for the supplied dev/test/prod accounts were checked.
- Lab 4 contains seven practical tasks and 22 required screenshot filenames.
- The comparison/Git-exclusion task and the PDF-preparation/two-repository-push task, including their seven screenshot entries, were removed.
- The instructor's `Labs/Lab04` directory contains only `README.md`.

Students edit `db_connect.py` and run `python db_connect.py` directly on Ubuntu. The workflow runs `python tests/verify_connections.py` as instructor verification.
