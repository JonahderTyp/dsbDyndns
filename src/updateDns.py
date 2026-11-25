import logging
import os
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv

from dns_client import DnsUpdateError, get_public_ip, update_dns


logger = logging.getLogger(__name__)


def configure_logging(log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"dyndns-{date.today().isoformat()}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )


def run_update(work_dir: Path) -> None:
    load_dotenv()
    current_ip = get_public_ip()
    if "TEST" in os.environ:
        logger.info("TEST IP: %s", current_ip)
        return

    ip_file = work_dir / "currentIP.txt"
    try:
        previous_ip = ip_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        previous_ip = None
        logger.info("No cached IP found; proceeding with DNS update")

    if current_ip == previous_ip:
        logger.info("Public IPv4 unchanged; skipping DNS update")
        return

    credentials = {name: os.getenv(name, "") for name in ("username", "password", "uid")}
    missing = [name for name, value in credentials.items() if not value]
    if missing:
        raise DnsUpdateError(f"Missing environment variables: {', '.join(missing)}")

    update_dns(current_ip, **credentials)
    ip_file.write_text(current_ip, encoding="utf-8")
    logger.info("Updated domain and subdomain to %s", current_ip)


def main() -> int:
    try:
        work_dir = Path.cwd()
        configure_logging(work_dir / "logs")
        run_update(work_dir)
    except (DnsUpdateError, OSError, UnicodeError, requests.RequestException) as error:
        logger.error("DNS update failed: %s", error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
