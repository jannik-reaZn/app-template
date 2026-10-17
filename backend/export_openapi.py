from pathlib import Path

import yaml

from main import app

OPENAPI_PATH = Path(__file__).resolve().parent.parent / "openapi.yaml"


def main() -> None:
    schema = app.openapi()
    OPENAPI_PATH.write_text(
        yaml.safe_dump(schema, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote {OPENAPI_PATH}")


if __name__ == "__main__":
    main()
