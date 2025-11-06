#!/usr/bin/env python3
import os
import sys

CONFIG_PATH = os.path.join("bmad", "bmm", "config.yaml")


def read_simple_yaml(path):
    config = {"user_name": "", "communication_language": "English", "output_folder": "outputs"}
    if not os.path.exists(path):
        return config
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, value = line.split(":", 1)
                    config[key.strip()] = value.strip()
    except Exception:
        pass
    return config


def main():
    cfg = read_simple_yaml(CONFIG_PATH)
    user = cfg.get("user_name", "Operator")
    lang = cfg.get("communication_language", "English")
    out = cfg.get("output_folder", "outputs")

    print(f"[switchd] NateOS starting (lang={lang})")
    print(f"[switchd] Hello, {user}!")
    print(f"[switchd] Outputs: {out}")
    print("[switchd] Loading components: dataplane, control-plane, mgmt-plane (stubs)")
    # Future: initialize Redis/datastore, start protocol daemons, expose mgmt API/CLI


if __name__ == "__main__":
    sys.exit(main())
