# Validation record

## Host Python integration verified

[GitHub Actions run 39252990522](https://github.com/WaqasSaleem97/Databases/actions/runs/39252990522) completed successfully on 19 October 2026 for source commit `7a5202784c19344083098568dee44e13ab98a148`.

Python 3.12 ran directly on the runner host. Docker Compose started only MySQL and the three MongoDB database services.

- Python database drivers installed successfully on the host.
- All 15 offline configuration and mocked database-boundary tests passed.
- The four database services initialized and passed their health checks.
- Host-side credential file preparation succeeded.
- All 11 live scenarios passed: MySQL, hardcoded MongoDB, three environment-variable profiles, three credential-file profiles, wrong-password rejection, missing-password rejection, and marker-mismatch write prevention.
- Disposable database services and volumes were removed after verification.

## Configuration and documentation checks

- Host endpoints are `127.0.0.1:3307` for MySQL and `127.0.0.1:27017`, `:27018` and `:27019` for MongoDB dev, test and simulated prod.
- Profile accounts and passwords agree with the database initialization settings.
- Python and JavaScript syntax, Compose configuration, health-check shell syntax, and the direct-host CI commands were checked.
- Lab 4 uses native Python commands and preserves its per-step screenshot format; its required filenames are synchronized with `evidence.json`.
- The Python application container, Dockerfile and Docker build instructions were removed.

Students should run `python -m unittest discover -s tests -v` and `python smoke_test.py` from their active host virtual environment after starting the databases and preparing their local credential files.
