from celery import Celery
from database import SessionLocal
import models

from scanner.nmap_scan import run_nmap
from scanner.subdomain import enumerate_subdomains
from scanner.dns_enum import dns_lookup
from redis_client import publish_update

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

def send_update(scan_id, status, data=None):
    payload = {
        "scan_id": scan_id,
        "status": status,
        "data": data
    }
    publish_update(scan_id, payload)


@celery.task
def run_full_scan(scan_id, target):
    db = SessionLocal()
    scan = db.query(models.Scan).get(scan_id)

    scan.status = "running"
    db.commit()

    send_update(scan_id, "running")

    # Step 1: Subdomains
    subs = enumerate_subdomains(target)
    send_update(scan_id, "subdomains_done", subs)

    # Step 2: DNS
    dns = dns_lookup(target)
    send_update(scan_id, "dns_done", dns)

    # Step 3: Nmap
    nmap = run_nmap(target)
    send_update(scan_id, "nmap_done", nmap)

    results = {
        "subdomains": subs,
        "dns": dns,
        "nmap": nmap
    }

    scan.status = "completed"
    scan.result = str(results)
    db.commit()

    send_update(scan_id, "completed", results)

    db.close()