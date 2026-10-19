# Validation Record

This revision reads the MongoDB username, password, endpoint and database name separately from process environment variables or an INI section. Python concatenates those values into `uri` before using the same MongoDB connection block.

Students continue to edit only `db_connect.py`. Python runs on the Ubuntu host, and Docker Compose runs the four database services.

## Verification Status

Live verification of this revision is pending. The workflow runs `python tests/verify_connections.py` against all eight successful stage/environment combinations, missing-variable rejection, wrong file-password rejection and file-section selection.

The verification harness is instructor support. The student run command remains `python db_connect.py`.
