# Validation Record

[GitHub Actions run 39261219705](https://github.com/WaqasSaleem97/Databases/actions/runs/39261219705) passed on 19 October 2026 for source commit `01d85309c7e5734158ff8bd72d9450b032d593a5`.

## Verified Behavior

Python 3.12 ran directly on the Ubuntu runner host. Docker Compose ran only MySQL and the three MongoDB database services.

- Both Python database drivers installed and the database-only Compose configuration passed validation.
- All four databases became healthy.
- All eight successful connections passed: MySQL, hardcoded MongoDB, three environment-variable profiles and three credential-file sections.
- The environment version read `MONGO_USERNAME`, `MONGO_PASSWORD`, `MONGO_ENDPOINT` and `MONGO_DATABASE` separately.
- The file version read separate `username`, `password`, `endpoint` and `database` fields.
- Each MongoDB example concatenated those values into `uri` and used the same connection block.
- Missing-variable rejection, wrong file-password rejection and default file-section selection passed.
- All 11 live scenarios passed, and the disposable database services and volumes were removed.

## Documentation Checks

- Both guides contain the same four short Python examples.
- Python and Bash syntax, navigation links, INI sections and export profiles were checked.
- URI construction preserved special characters in credentials through percent encoding.
- Screenshot display commands redacted the sample passwords.
- The nine task screenshot lists were preserved.
- Explanations describe Python connection settings without cross-language comparisons.
- The instructor's `Labs/Lab04` directory contains only `README.md`; students put written answers in `Lab4_Solution.pdf`.

Students edit `db_connect.py` and run `python db_connect.py` on Ubuntu. The workflow runs `python tests/verify_connections.py` as instructor verification.
