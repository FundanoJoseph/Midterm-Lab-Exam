"""Configuration management: load settings from an external JSON file.

Environment variables (cloud-friendly) can override file values:
  SIS_DATA_FILE, SIS_LOG_LEVEL
"""
import json
import os

DEFAULT_CONFIG = {
    "app_name": "Student Information System",
    "version": "1.0.0",
    "data_file": "data/students.json",
    "export_dir": "data/exports",
    "logging": {"level": "INFO", "file": "logs/app.log",
                "max_bytes": 1048576, "backup_count": 3},
}


def load_config(path: str = "config/config.json") -> dict:
    """Load config from `path`; fall back to defaults if missing/invalid."""
    config = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
    try:
        with open(path, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        for key, value in user_cfg.items():
            if isinstance(value, dict) and isinstance(config.get(key), dict):
                config[key].update(value)
            else:
                config[key] = value
    except FileNotFoundError:
        print(f"[warn] Config file '{path}' not found. Using defaults.")
    except json.JSONDecodeError as exc:
        print(f"[warn] Config file invalid ({exc}). Using defaults.")

    # Environment overrides (useful for cloud deployments)
    config["data_file"] = os.getenv("SIS_DATA_FILE", config["data_file"])
    config["logging"]["level"] = os.getenv("SIS_LOG_LEVEL",
                                           config["logging"]["level"])
    return config
