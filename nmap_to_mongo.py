#!/usr/bin/env python3
import sys
import nmap
from pymongo import MongoClient
from datetime import datetime, timezone

def connect_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["redteam_tracker"]
    return db

def scan_and_import(target_subnet):
    db = connect_db()
    nm = nmap.PortScanner()
    
    print(f"[*] Starting intense Nmap scan on: {target_subnet}...")
    nm.scan(hosts=target_subnet, arguments="-sV -O")
    
    if not nm.all_hosts():
        print(f"[-] No hosts found at {target_subnet}. The machine might be down or blocking ping.")
        return
    
    for host in nm.all_hosts():
        ip = host
        state = nm[host].state()
        domain = nm[host].hostname() if nm[host].hostname() else "N/A"
        
        os_name = "Unknown"
        if 'osmatch' in nm[host] and len(nm[host]['osmatch']) > 0:
            os_name = nm[host]['osmatch'][0]['name']

        ports_list = []
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                port_data = nm[host][proto][port]
                if port_data['state'] == 'open':
                    ports_list.append({
                        "port_number": int(port),
                        "protocol": proto,
                        "service_name": port_data['name'],
                        "service_version": f"{port_data['product']} {port_data['version']}".strip(),
                        "state": port_data['state']
                    })

        # 1. UPSERT the Current State
        target_document = {
            "ip_address": ip,
            "domain_name": domain,
            "operating_system": os_name,
            "status": state,
            "last_seen": datetime.now(timezone.utc),
            "open_ports": ports_list
        }

        db.targets.update_one(
            {"ip_address": ip},
            {"$set": target_document},
            upsert=True
        )
        
        # 2. INSERT the Historical State
        target_record = db.targets.find_one({"ip_address": ip})
        
        history_document = {
            "target_id": target_record["_id"],
            "scanned_at": datetime.now(timezone.utc),
            "scan_parameters": "-sV -O",
            "status_at_time": state,
            "ports_found": ports_list
        }
        
        db.scan_history.insert_one(history_document)
        
        print(f"[+] Sync'd {ip} to targets AND logged to scan_history.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 nmap_to_mongo.py <target_ip_or_subnet>")
        sys.exit(1)
        
    scan_target = sys.argv[1]
    scan_and_import(scan_target)
