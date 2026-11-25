import logging
from ipaddress import IPv4Address

import requests


logger = logging.getLogger(__name__)

BASE_URL = "https://mein.domainssaubillig.de"
REQUEST_TIMEOUT = 10
LOGIN_FORM_MARKER = b'id="tl_login"'
SIGN_IN_REQUIRED = b"Bitte melden Sie sich im Kundenbereich an"


class DnsUpdateError(Exception):
    pass


def get_public_ip() -> str:
    logger.info("Looking up the public IPv4 via api.ipify.org")
    response = requests.get("https://api.ipify.org", timeout=REQUEST_TIMEOUT)
    logger.info("Public IPv4 service returned HTTP %d", response.status_code)
    response.raise_for_status()
    try:
        ip = str(IPv4Address(response.text.strip()))
    except ValueError as error:
        raise DnsUpdateError("Public IP service did not return a valid IPv4 address") from error
    logger.info("Public IPv4: %s", ip)
    return ip


def update_dns(ip: str, *, username: str, password: str, uid: str) -> None:
    with requests.Session() as session:
        logger.info("Signing in to the DNS provider")
        login = session.post(
            f"{BASE_URL}/interface.html",
            data={"FORM_SUBMIT": "tl_login", "username": username, "password": password},
            timeout=REQUEST_TIMEOUT,
        )
        logger.info("Provider sign-in returned HTTP %d", login.status_code)
        login.raise_for_status()
        if LOGIN_FORM_MARKER in login.content:
            raise DnsUpdateError("Provider returned the sign-in form after login; check your .env credentials")

        payload = {"uid": uid, "formf": "919", "ipv4": ip, "ipv6": ""}
        failures = []
        for target, endpoint, record_id in (
            ("domain", "editdns.php", {"did": "140014"}),
            ("subdomain", "sub_editdns.php", {"sdid": "198516"}),
        ):
            logger.info("Submitting %s IPv4 update via /%s", target, endpoint)
            try:
                response = session.post(
                    f"{BASE_URL}/{endpoint}",
                    data={**payload, **record_id},
                    headers={"Origin": BASE_URL},
                    timeout=REQUEST_TIMEOUT,
                )
            except requests.RequestException as error:
                failures.append(f"{target}: {type(error).__name__}")
            else:
                logger.info("Provider returned HTTP %d for the %s update", response.status_code, target)
                if response.status_code == 403 and SIGN_IN_REQUIRED in response.content:
                    failures.append(f"{target}: HTTP 403 (provider requires a signed-in session)")
                elif not response.ok:
                    failures.append(f"{target}: HTTP {response.status_code}")
                elif b"erfolgreich" not in response.content:
                    failures.append(f"{target}: provider did not confirm the update")
                else:
                    logger.info("Provider confirmed the %s update", target)

        if failures:
            raise DnsUpdateError("; ".join(failures))
