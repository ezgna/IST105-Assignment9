# dna_center_cisco/dnac_manager.py

import requests
from requests.auth import HTTPBasicAuth
from .dnac_config import DNAC
import urllib3

urllib3.disable_warnings()


class DNAC_Manager:
    def __init__(self):
        self.token = None

    def get_auth_token(self):
        """Authenticates to DNA Center and stores token. Returns True/False."""
        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/dna/system/api/v1/auth/token"
            response = requests.post(
                url,
                auth=HTTPBasicAuth(DNAC["username"], DNAC["password"]),
                verify=False,
                timeout=10,
            )
            response.raise_for_status()
            self.token = response.json()["Token"]
            return True
        except Exception as e:
            print(f"[DNAC] Authentication failed: {e}")
            self.token = None
            return False

    def get_network_devices(self):
        """Returns list of devices or None"""
        if not self.token:
            print("[DNAC] No token, authenticate first")
            return None

        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/network-device"
            headers = {"X-Auth-Token": self.token}
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            response.raise_for_status()
            return response.json().get("response", [])
        except Exception as e:
            print(f"[DNAC] Failed to get devices: {e}")
            return None

    def get_device_interfaces(self, device_ip):
        """Returns list of interfaces for given device_ip, or None"""
        if not self.token:
            print("[DNAC] No token, authenticate first")
            return None

        try:
            # Get all devices
            devices = self.get_network_devices()
            if not devices:
                return None

            # Find the device by management IP
            device = next(
                (d for d in devices if d.get("managementIpAddress") == device_ip), None
            )
            if not device:
                print(f"[DNAC] Device {device_ip} not found")
                return None

            # Fetch interfaces by deviceId
            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/interface"
            headers = {"X-Auth-Token": self.token}
            params = {"deviceId": device["id"]}
            response = requests.get(
                url, headers=headers, params=params, verify=False, timeout=10
            )
            response.raise_for_status()
            return response.json().get("response", [])
        except Exception as e:
            print(f"[DNAC] Failed to get interfaces: {e}")
            return None