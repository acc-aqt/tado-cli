"""Provide an exemplary entry point."""

import requests
import subprocess
from utils import api_call

ME_URL = "https://my.tado.com/api/v2/me"
DEVICES_URL = "https://my.tado.com/api/v2/homes/{}/devices"
OFFSET_URL = "https://my.tado.com/api/v2/devices/{}/temperatureOffset"

TOKEN_URL = "https://login.tado.com/oauth2/token"
CLIENT_ID = "1bb50063-6b0c-4d11-bd99-387f4a91cc46"

BROWSER = "Safari"

class TadoClient():
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.home_id = None
        device_ids = ["VA0452158976", "VA3622987264", "VA3857868288"]

        
        self.renew_access_tokens()
        
        me = api_call("https://my.tado.com/api/v2/me", self.access_token)
        print(me)
        self.home_id = me["homes"][0]["id"]
        
        print(self.home_id)
        
        # devices = api_call(f"https://my.tado.com/api/v2/homes/{self.home_id}/devices", self.access_token)

        for device in device_ids:
            offset = api_call(f"https://my.tado.com/api/v2/devices/{device}/temperatureOffset", self.access_token)
            print(f"Device {device} offset: {offset}")
            
            api_call(f"https://my.tado.com/api/v2/devices/{device}/temperatureOffset", self.access_token, r_type="PUT", data={"celsius": -4.0})
            
            offset = api_call(f"https://my.tado.com/api/v2/devices/{device}/temperatureOffset", self.access_token)
            print(f"Device {device} offset: {offset}")

            
            
        
        
    
    @staticmethod
    def _refresh_access_token(refresh_token: str):
        r = requests.post(
            TOKEN_URL,
            data={
                "client_id": CLIENT_ID,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()  # contains access_token, expires_in, (maybe) refresh_token

    @staticmethod
    def _initiate_device_code_flow():
        response = requests.post(
        "https://login.tado.com/oauth2/device_authorize",
        timeout=30,
        params=dict(
            client_id=CLIENT_ID,
            scope="offline_access",
        ))
        
        verifiaction_uri = response.json()['verification_uri_complete']
        print(f"Please visit {verifiaction_uri} to authorize the device.")
        subprocess.Popen(["open", "-a", BROWSER, verifiaction_uri])
        device_code = response.json()['device_code']
        print(f"Device code: {device_code}")
        return device_code
    
    

    def _store_tokens(self, device_code: str):
        response = requests.post(
            "https://login.tado.com/oauth2/token",
            params=dict(
                client_id=CLIENT_ID,
                device_code=device_code,
                grant_type="urn:ietf:params:oauth:grant-type:device_code",
            )
        )
        
        print(f"Access Token Response: {response.json()}")
        self.access_token = response.json().get("access_token")
        self.refresh_token = response.json().get("refresh_token")
        #write_env_var("TADO_REFRESH_TOKEN", refresh_token)


    def get_weather(self, home_id: str):
        WEATHER_URL = f"https://my.tado.com/api/v2/homes/{home_id}/weather"
        api_response = api_call(WEATHER_URL, self.access_token)
        print(api_response)



    def renew_access_tokens(self):
        device_code = self._initiate_device_code_flow()
        input("Press ENTER after you have completed authorization...")
        self._store_tokens(device_code)
    
def main() -> None:
    
    client = TadoClient()

if __name__ == "__main__":
    
    main()