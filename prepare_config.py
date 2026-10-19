"""Copy dummy templates to ignored config files; never overwrite an existing file."""

from pathlib import Path


root = Path(__file__).resolve().parent
destination = root / "config"
destination.mkdir(exist_ok=True)
for environment in ("dev", "test", "prod"):
    target = destination / f"{environment}.ini"
    try:
        with target.open("x", encoding="utf-8") as stream:
            stream.write((root / "config-examples" / f"{environment}.ini.example").read_text(encoding="utf-8"))
        target.chmod(0o600)
        print(f"Created config/{environment}.ini")
    except FileExistsError:
        print(f"Kept existing config/{environment}.ini")
