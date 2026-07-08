#!/usr/bin/env python3
import sys
import hashlib
import getpass
from pymongo import MongoClient

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_vulnerability(ip, cve, title, severity):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["redteam_tracker"]
    
    # --- AUTHENTICATION PHASE ---
    print("\n--- SECURE LOGIN REQUIRED ---")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    
    user_record = db.users.find_one({"username": username})
    
    if not user_record or user_record["password_hash"] != hash_password(password):
        print("[-] Access Denied: Invalid credentials.")
        return
        
    # --- AUTHORIZATION PHASE ---
    if user_record["role"] != "Lead_Operator":
        print(f"[-] Access Denied: Role '{user_record['role']}' is not authorized to add vulnerabilities.")
        return
        
    print("[+] Authentication and Authorization successful.\n")
    
    # --- DATABASE INSERTION PHASE ---
    target = db.targets.find_one({"ip_address": ip})
    if not target:
        print(f"[-] Target {ip} not found in database. Scan it first!")
        return
        
    vuln_doc = {
        "target_id": target["_id"],
        "cve_id": cve,
        "title": title,
        "severity": severity,
        "is_exploited": False,
        "reported_by": username  # Audit trail: who added this?
    }
    
    db.vulnerabilities.insert_one(vuln_doc)
    print(f"[+] Vulnerability '{title}' successfully linked to {ip} by {username}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 add_vuln.py    <severity>")
        sys.exit(1)
        
    add_vulnerability(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
