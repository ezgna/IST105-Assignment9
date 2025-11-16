from django.shortcuts import render
from django.http import HttpRequest
from .dnac_manager import DNAC_Manager
from .mongo_logger import log_interaction

# Reuse a single DNAC_Manager instance for simplicity
dnac_manager = DNAC_Manager()


def auth_view(request: HttpRequest):
    """
    View for obtaining and displaying the DNA Center authentication token.

    URL: /auth/
    """
    success = dnac_manager.get_auth_token()
    token = dnac_manager.token if success else None

    # Log interaction to MongoDB
    log_interaction(action="auth", device_ip=None, success=success)

    context = {
        "success": success,
        "token": token,
    }
    return render(request, "dna_center_cisco/auth.html", context)


def devices_view(request: HttpRequest):
    """
    View for displaying the list of network devices.

    URL: /devices/
    """
    # Try to authenticate if we don't have a token yet
    if not dnac_manager.token:
        dnac_manager.get_auth_token()

    devices = dnac_manager.get_network_devices()
    success = devices is not None

    # Log interaction to MongoDB
    log_interaction(action="devices", device_ip=None, success=success)

    context = {
        "success": success,
        "devices": devices or [],
    }
    return render(request, "dna_center_cisco/devices.html", context)


def interfaces_view(request: HttpRequest):
    """
    View for displaying interface details for a specific device IP.

    URL example: /interfaces/?ip=10.10.20.1
    The device IP can be provided either as a query parameter or via POST form.
    """
    device_ip = request.GET.get("ip") or request.POST.get("ip")
    interfaces = []
    success = False

    # Try to authenticate if we don't have a token yet
    if not dnac_manager.token:
        dnac_manager.get_auth_token()

    if device_ip:
        interfaces = dnac_manager.get_device_interfaces(device_ip)
        success = interfaces is not None

        # Log interaction to MongoDB
        log_interaction(
            action="interfaces",
            device_ip=device_ip,
            success=success,
        )

    context = {
        "device_ip": device_ip,
        "interfaces": interfaces or [],
        "success": success,
    }
    return render(request, "dna_center_cisco/interfaces.html", context)