# Validation record

Checked on 19 October 2026 with Python 3.12.14, PyMongo 4.19.0, MySQL Connector/Python 9.7.0, and dnspython 2.9.0.

- All 15 offline tests passed. These cover missing configuration, distinct profiles, literal special characters in passwords, file selection, masked representations, safe error messages, and blocking MongoDB writes when the database marker is missing or incorrect.
- All Python files parsed successfully; the MongoDB seed JavaScript passed Node's syntax check.
- The Docker-based revision has five Compose services: the Python app plus four databases. Its service-name endpoints, loopback-only published database ports, health-check shell syntax, and agreement between provisioning accounts and configuration templates are checked locally.
- Config preparation was run twice: the second run kept existing files rather than overwriting them.
- The stage 4 command-line help rendered successfully.

**Live integration was not executed:** this preparation environment has no Docker/Podman engine or MySQL/MongoDB server binaries. The Compose services were not started here. The YAML check is not an engine-level Compose validation. Driver/network behavior and database initialization still need the provided live smoke test on the teaching machine.

Run the Docker setup, `docker compose run --rm app python prepare_config.py`, then `docker compose run --rm app python smoke_test.py`. The live check performs eight successful stage/environment runs and three expected failure scenarios against the local lab databases. The included GitHub Actions workflow also builds and exercises this complete Docker setup. It uses only disposable classroom data.
