import requests
from pathlib import Path

ENV_PATH = Path(".env")


def api_call(endpoint, access_token, r_type="GET", data=None):
    headers = {"Authorization": f"Bearer {access_token}"}

    if r_type == "GET":
        r = requests.get(endpoint, headers=headers)
    elif r_type == "PUT":
        r = requests.put(endpoint, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported request type: {r_type}")

    r.raise_for_status()
    return r.json()

def write_env_var(key: str, value: str):
    lines = []

    if ENV_PATH.exists():
        lines = ENV_PATH.read_text().splitlines()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            updated = True
            break

    if not updated:
        lines.append(f"{key}={value}")

    ENV_PATH.write_text("\n".join(lines) + "\n")