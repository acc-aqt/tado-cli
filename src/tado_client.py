"""Contains TadoClient class for interacting with Tado API."""

import subprocess

import requests

from utils import api_call

BROWSER = "Safari"


class TadoClient:
    """Client for Tado API interactions."""

    CLIENT_ID = "1bb50063-6b0c-4d11-bd99-387f4a91cc46"  # Public client ID, does not need to be secret

    def __init__(self) -> None:
        self.access_token = None
        self.refresh_token = None
        self.home_id = None

        self._renew_access_tokens()

        me_response = api_call(
            "https://my.tado.com/api/v2/me", self.access_token
        )
        self.home_id = me_response["homes"][0]["id"]

    def get_thermostat_ids(self) -> list[str]:
        """Retrieve thermostat device IDs."""
        devices_response = api_call(
            f"https://my.tado.com/api/v2/homes/{self.home_id}/devices",
            self.access_token,
        )

        thermostat_ids = []
        for d in devices_response:
            if not d.get("deviceType", "").startswith("VA"):
                continue
            caps = d.get("characteristics", {}).get("capabilities", [])
            if "INSIDE_TEMPERATURE_MEASUREMENT" in caps:
                thermostat_ids.append(d["serialNo"])

        return thermostat_ids

    def set_temperature_offset(
        self, device: str, offset_value: float = -4.0
    ) -> None:
        """Set temperature offset for a specific device."""
        offset = api_call(
            f"https://my.tado.com/api/v2/devices/{device}/temperatureOffset",
            self.access_token,
        )
        print(f"Device {device} offset before update: {offset}")

        api_call(
            f"https://my.tado.com/api/v2/devices/{device}/temperatureOffset",
            self.access_token,
            r_type="PUT",
            data={"celsius": offset_value},
        )

        offset = api_call(
            f"https://my.tado.com/api/v2/devices/{device}/temperatureOffset",
            self.access_token,
        )
        print(f"Device {device} offset after update: {offset}")

    def _renew_access_tokens(self) -> None:
        device_code = self._initiate_device_code_flow()
        input("Press ENTER after you have completed authorization...")
        self._store_tokens(device_code)

    @staticmethod
    def _initiate_device_code_flow() -> str:
        response = requests.post(
            "https://login.tado.com/oauth2/device_authorize",
            timeout=30,
            params={
                "client_id": TadoClient.CLIENT_ID,
                "scope": "offline_access",
            },
        )

        verifiaction_uri = response.json()["verification_uri_complete"]
        print(f"Visiting {verifiaction_uri} to authorize the device...")

        subprocess.Popen(["open", "-a", BROWSER, verifiaction_uri])

        return response.json()["device_code"]

    def _store_tokens(self, device_code: str) -> None:
        response = requests.post(
            "https://login.tado.com/oauth2/token",
            timeout=30,
            params={
                "client_id": TadoClient.CLIENT_ID,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
        )

        self.access_token = response.json().get("access_token")
        self.refresh_token = response.json().get("refresh_token")
