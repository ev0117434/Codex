import json

from snapshot.config_loader import load_simple_yaml


def get_status(config_path: str = "config/config.yaml") -> dict[str, str]:
    config = load_simple_yaml(config_path)
    return {
        "status": config.get("health", {}).get("status", "unknown"),
        "service": config.get("app", {}).get("name", "unknown"),
    }


if __name__ == "__main__":
    print(json.dumps(get_status(), ensure_ascii=False))
