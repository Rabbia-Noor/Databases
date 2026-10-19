# Validation record

The current revision runs Python directly on the Ubuntu host. Docker Compose defines only MySQL and the three MongoDB services.

## Verification

- The 15 offline tests cover profile selection, required settings, literal password characters, safe error messages and blocking MongoDB writes when the database marker is wrong or missing.
- The live smoke test covers eight successful stage/environment combinations and three expected failures, using the host-published ports.
- The GitHub Actions workflow installs Python drivers on its host runner and runs the same offline and live checks against the database containers.

The preparation machine has no Docker engine. The live result for this host-based revision will be recorded after its GitHub Actions run completes.

Students can run `python -m unittest discover -s tests -v` and `python smoke_test.py` from their active host virtual environment after starting the databases and preparing the local credential files.
