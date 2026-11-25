from ipaddress import IPv4Address

import requests


BASE_URL = "https://mein.domainssaubillig.de"
REQUEST_TIMEOUT = 10


class DnsUpdateError(Exception):
    pass


def get_public_ip() -> str:
    response = requests.get("https://api.ipify.org", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    try:
        return str(IPv4Address(response.text.strip()))
    except ValueError as error:
        raise DnsUpdateError("Public IP service did not return a valid IPv4 address") from error


def update_dns(ip: str, *, username: str, password: str, uid: str) -> None:
    with requests.Session() as session:
        login = session.post(
            f"{BASE_URL}/interface.html",
            data={"FORM_SUBMIT": "tl_login", "username": username, "password": password},
            timeout=REQUEST_TIMEOUT,
        )
        login.raise_for_status()

        payload = {"uid": uid, "formf": "919", "ipv4": ip, "ipv6": ""}
        failures = []
        for target, endpoint, record_id in (
            ("domain", "editdns.php", {"did": "140014"}),
            ("subdomain", "sub_editdns.php", {"sdid": "198516"}),
        ):
            try:
                response = session.post(
                    f"{BASE_URL}/{endpoint}",
                    data={**payload, **record_id},
                    timeout=REQUEST_TIMEOUT,
                )
            except requests.RequestException as error:
                failures.append(f"{target}: {type(error).__name__}")
            else:
                if not response.ok:
                    failures.append(f"{target}: HTTP {response.status_code}")
                elif b"erfolgreich" not in response.content:
                    failures.append(f"{target}: provider did not confirm the update")

        if failures:
            raise DnsUpdateError("; ".join(failures))
