"""Tado API Client to adjust temperature offsets for devices."""

import subprocess

import requests

from utils import api_call

BROWSER = "Safari"
CLIENT_ID = "1bb50063-6b0c-4d11-bd99-387f4a91cc46"


class TadoClient:
    """Client for Tado API interactions."""

    def __init__(self) -> None:
        self.access_token = None
        self.refresh_token = None
        self.home_id = None

        self._renew_access_tokens()

        me_response = api_call(
            "https://my.tado.com/api/v2/me", self.access_token
        )
        self.home_id = me_response["homes"][0]["id"]

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
            params={"client_id": CLIENT_ID, "scope": "offline_access"},
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
                "client_id": CLIENT_ID,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
        )

        self.access_token = response.json().get("access_token")
        self.refresh_token = response.json().get("refresh_token")


def main() -> None:
    """Instantiate TadoClient and set temperature offsets for devices."""
    client = TadoClient()

    device_ids = ["VA0452158976", "VA3622987264", "VA3857868288"]

    for device in device_ids:
        client.set_temperature_offset(device, offset_value=-4.0)


if __name__ == "__main__":
    main()
