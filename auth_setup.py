#!/usr/bin/env python3
import hashlib
from pymongo import MongoClient

def hash_password(password):
    # Never store plain-text passwords! Use SHA-256 hashing.
    return hashlib.sha256(password.encode()).hexdigest()

def setup_users():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["redteam_tracker"]
    
    # Enforce unique usernames at the database level
    db.users.create_index("username", unique=True)
    
    users_to_add = [
        {
            "username": "zuni_admin",
            "password_hash": hash_password("admin123"),
            "role": "Lead_Operator"
        },
        {
            "username": "guest_analyst",
            "password_hash": hash_password("guest123"),
            "role": "Analyst"
        }
    ]
    
    try:
        db.users.insert_many(users_to_add)
        print("[+] Successfully created 'users' collection.")
        print("[+] Added Lead_Operator (zuni_admin) and Analyst (guest_analyst).")
    except Exception as e:
        print("[-] Users likely already exist or an error occurred:", e)

if __name__ == "__main__":
    setup_users()
