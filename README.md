# 🕸️ SpectralGraph: NoSQL Red Team Asset Tracker

**SpectralGraph** is an automated, NoSQL-backed database application designed to replace static spreadsheets in cybersecurity Red Team operations. Built on **MongoDB** and **Python**, it automatically ingests hierarchical network scan data, tracks infrastructure state changes over time, and securely maps identified CVEs to specific targets.

*Developed as a 4th-Semester BSc Computer Science Project at Abbottabad University of Science & Technology (AUST).*

---

## Core Architecture & Features

* **Hybrid NoSQL Schema:** Uses **Embedding** (storing open ports directly inside target documents for rapid reads) and **Referencing** (linking vulnerabilities to targets to normalize data).
* **Idempotent Data Ingestion:** Automates Nmap scanning via Python. Uses PyMongo `upsert=True` logic to update existing network assets without creating duplicate database records.
* **Time-Series Audit Logging:** Every scan concurrently writes an immutable timestamped log to the `scan_history` collection, maintaining a permanent record of network state changes.
* **Role-Based Access Control (RBAC):** Application-layer security secures the database. Operator credentials are encrypted using **SHA-256 Hashing**. Only `Lead_Operator` accounts can perform vulnerability database writes.
* **Advanced Aggregation Pipelines:** Replaces standard read queries with a 4-stage NoSQL pipeline (`$lookup`, `$unwind`, `$group`, `$sort`) to act as a relational `LEFT JOIN`, generating executive analytics grouped by Operating System.

---

## Technology Stack
* **Database Engine:** MongoDB 7.0 (NoSQL Document Store)
* **Logic / Backend:** Python 3.11+
* **Libraries:** `pymongo`, `python-nmap`, `hashlib`
* **Environment:** Kali Linux / Windows Subsystem for Linux (WSL)

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/SpectralGraph.git](https://github.com/YOUR_USERNAME/SpectralGraph.git)
   cd SpectralGraph
   Start the MongoDB Server:
1)
Bash
sudo systemctl start mongod
Install Dependencies:
2)
Bash
pip install -r requirements.txt
Execution Guide
1. Initialize Security Roles (RBAC)
Creates the users collection and generates hashed admin and analyst credentials.

Bash
python3 auth_setup.py
2. Automated Data Ingestion
Scans a target and upserts data into the targets and scan_history collections.

Bash
sudo python3 nmap_to_mongo.py 10.0.2.15
3. Test Security (Insert Vulnerability)
Attempts to insert a CVE. Log in as zuni_admin to succeed, or guest_analyst to be blocked.

Bash
python3 add_vuln.py 10.0.2.15 "CVE-2024-3094" "XZ Utils" "Critical"
4. Execute Aggregation Pipeline (Analytics)
Runs the 4-stage MongoDB pipeline to generate a dashboard grouping targets by OS and tallying vulnerabilities.

Bash
python3 network_analytics.py
