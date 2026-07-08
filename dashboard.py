#!/usr/bin/env python3
from pymongo import MongoClient

def generate_dashboard():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["redteam_tracker"]
    
    # The Aggregation Pipeline
    pipeline = [
        {
            # $lookup acts exactly like a SQL LEFT JOIN
            "$lookup": {
                "from": "vulnerabilities",
                "localField": "_id",       # The ID in the targets collection
                "foreignField": "target_id", # The ID in the vulnerabilities collection
                "as": "linked_vulns"         # The name of the new temporary array
            }
        },
        {
            # $project formats the final output so it's clean
            "$project": {
                "_id": 0,
                "ip_address": 1,
                "operating_system": 1,
                "total_vulns": { "$size": "$linked_vulns" },
                "cve_list": "$linked_vulns.cve_id"
            }
        }
    ]
    
    print("\n" + "="*50)
    print(" 🎯 RED TEAM ASSET & VULNERABILITY DASHBOARD")
    print("="*50)
    
    # Run the pipeline
    results = db.targets.aggregate(pipeline)
    
    for host in results:
        ip = host.get("ip_address", "Unknown")
        os = host.get("operating_system", "Unknown")
        vuln_count = host.get("total_vulns", 0)
        
        # Format the CVE list beautifully
        if vuln_count > 0:
            cves = ", ".join(host.get("cve_list", []))
        else:
            cves = "None Detected"
            
        print(f"[+] Target IP : {ip}")
        print(f"    OS        : {os}")
        print(f"    Vuln Count: {vuln_count}")
        print(f"    Known CVEs: {cves}")
        print("-" * 50)

if __name__ == "__main__":
    generate_dashboard()
