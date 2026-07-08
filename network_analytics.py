#!/usr/bin/env python3
from pymongo import MongoClient

def run_analytics():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["redteam_tracker"]

    # This is a 4-stage NoSQL Aggregation Pipeline
    pipeline = [
        # Stage 1 ($lookup): Join the targets and vulnerabilities collections
        {
            "$lookup": {
                "from": "vulnerabilities",
                "localField": "_id",
                "foreignField": "target_id",
                "as": "vuln_data"
            }
        },
        # Stage 2 ($unwind): Deconstruct the array so each vulnerability gets its own row for counting
        {
            "$unwind": "$vuln_data"
        },
        # Stage 3 ($group): Group the data by Operating System AND Severity, then count them
        {
            "$group": {
                "_id": {
                    "os": "$operating_system",
                    "severity": "$vuln_data.severity"
                },
                "count": { "$sum": 1 }
            }
        },
        # Stage 4 ($sort): Order alphabetically by OS, then by highest count
        {
            "$sort": { "_id.os": 1, "count": -1 }
        }
    ]

    print("\n" + "="*60)
    print(" 📊 NETWORK SECURITY ANALYTICS: VULNERABILITIES BY OS")
    print("="*60)

    results = db.targets.aggregate(pipeline)

    current_os = None
    count = 0
    for result in results:
        count += 1
        os_name = result["_id"]["os"]
        severity = result["_id"]["severity"]
        vuln_count = result["count"]

        # Print a header if it's a new Operating System in the loop
        if os_name != current_os:
            print(f"\n[+] Operating System: {os_name}")
            current_os = os_name
        
        print(f"    -> {severity} Severity: {vuln_count} CVE(s)")
        
    if count == 0:
        print("\n[-] No vulnerabilities found to aggregate.")
        
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    run_analytics()
