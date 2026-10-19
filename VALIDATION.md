# Validation record

Verified on 19 October 2026. Local preparation used Python 3.12.14, PyMongo 4.19.0, MySQL Connector/Python 9.7.0, and dnspython 2.9.0.

## Live Docker verification

[GitHub Actions run 39249736356](https://github.com/WaqasSaleem97/Databases/actions/runs/39249736356) completed successfully for source commit `44f86b8c8b78d282ef32b426b8af67eca2e50125`.

- Docker Compose configuration validation and the Python application image build passed.
- All 15 configuration and mocked database-boundary tests passed inside the application container.
- MySQL and all three MongoDB services started and passed their health checks.
- Local dummy credential files were prepared successfully through the application container.
- All 11 live scenarios passed: eight successful stage/environment combinations, wrong-password rejection, missing-password rejection, and blocking a write when the database marker does not match the selected environment.
- The workflow removed the disposable services and data volumes after verification.

## Additional local checks

- All Python files parsed successfully; the MongoDB seed JavaScript passed Node's syntax check.
- Five Compose services, internal service-name endpoints, loopback-only host bindings, health-check shell syntax, and matching provisioning/profile credentials were checked.
- Config preparation was run twice; the second run preserved existing files.
- Screenshot source-viewing commands redact passwords before capture.
- Lab 4's 37 mandatory evidence filenames, task navigation, submission rules and PDF Git exception were checked.

The preparation machine itself has no Docker engine. Live integration was therefore verified on the GitHub Actions runner. Students should still run the documented Docker setup and `docker compose run --rm app python smoke_test.py` on their own machines before submitting evidence.
