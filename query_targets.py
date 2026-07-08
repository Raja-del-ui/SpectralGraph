#!/usr/bin/env python3
import sys
from pymongo import MongoClient

def search_by_port(port_number):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["redteam_tracker"]
    
    print(f"\n[*] Searching database for targets with port {port_number} open...\n")
    
    # MongoDB Query: Find documents where the 'open_ports' array 
    # contains a sub-document with the matching port_number
    query = {"open_ports": {"$elemMatch": {"port_number": port_number}}}
    
    results = db.targets.find(query)
    count = 0
    
    for target in results:
        count += 1
        ip = target.get("ip_address", "Unknown IP")
        os = target.get("operating_system", "Unknown OS")
        
        # Extract just the specific service running on that port
        service_info = "Unknown Service"
        for p in target.get("open_ports", []):
            if p["port_number"] == port_number:
                service_info = p.get("service_version", p.get("service_name", "Unknown"))
        
        print(f"[+] Target: {ip}")
        print(f"    OS: {os}")
        print(f"    Service on {port_number}: {service_info}")
        print("-" * 40)
        
    if count == 0:
        print(f"[-] No targets found with port {port_number} open.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_targets.py <port_number>")
        sys.exit(1)
        
    try:
        target_port = int(sys.argv[1])
        search_by_port(target_port)
    except ValueError:
        print("Error: Port must be a number.")
