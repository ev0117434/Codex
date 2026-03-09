from pathlib import Path


def load_simple_yaml(path: str) -> dict:
    data: dict = {}
    section = None
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith("  ") and line.endswith(":"):
            section = line[:-1].strip()
            data[section] = {}
            continue
        if line.startswith("  ") and ":" in line and section:
            key, value = line.strip().split(":", 1)
            value = value.strip()
            if value.lower() == "true":
                parsed = True
            elif value.lower() == "false":
                parsed = False
            else:
                parsed = value
            data[section][key] = parsed
    return data
