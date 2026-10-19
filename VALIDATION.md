# Validation Record

This revision teaches four short examples by editing only `db_connect.py`:

- MySQL with hardcoded connection arguments.
- MongoDB with a hardcoded URI and database name.
- The same MongoDB connection block using `os.getenv()`.
- The same MongoDB connection block using sections in `credentials.ini`.

Python runs on the Ubuntu host. Compose runs only the four database services.

## Current Verification

Static syntax, example consistency, screenshot filenames and shell-command checks are run before publishing. Live verification for this simplified revision is pending; the previous multi-file implementation's test results do not apply to this revision.

The GitHub Actions workflow runs `python tests/verify_connections.py` on the host against the database containers. It checks eight successful connections (MySQL, hardcoded MongoDB, three environment-variable profiles and three file sections), missing-variable rejection, wrong-password rejection and file-source selection.

Students edit only `db_connect.py` and create their local credential-file copy. The verification harness is instructor support.
