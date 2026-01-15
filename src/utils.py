"""Module containing utility functions."""

import requests


def api_call(
    endpoint: str, access_token: str, r_type: str = "GET", data: dict = None
) -> dict:
    """Perform an API call to the specified endpoint with the given access token."""
    headers = {"Authorization": f"Bearer {access_token}"}

    if r_type == "GET":
        r = requests.get(endpoint, headers=headers, timeout=30)
    elif r_type == "PUT":
        r = requests.put(endpoint, headers=headers, json=data, timeout=30)
    else:
        raise ValueError(f"Unsupported request type: {r_type}")

    r.raise_for_status()
    return r.json()
