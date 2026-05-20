# 🛡️ User-Friendly System Call Interface for Enhanced Security

[![GitHub stars](https://img.shields.io/github/stars/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security.svg?style=social)](https://github.com/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security/stargazers)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🔎 Project Overview

Secure System Call Interface (Enhanced Security File Manager) is a web-based platform designed to **perform system-level operations safely** (like file management and process execution) via a controlled interface — with **authentication, role-based authorization, encryption, and comprehensive logging**.  
It acts as a “gateway” for system calls, ensuring unauthorized or malicious operations are prevented, and all activity is auditable.

**Why this project matters:**

- Most native system calls expose powerful operations — misuse could compromise the system.  
- This interface restricts those operations to authorized users only.  
- Detailed logs + audit trails + optional analytics help administrators monitor usage and detect suspicious behavior.  

---

## 🚀 Quick Start & Installation

Getting this project running locally is very simple because the Flask backend automatically serves all the frontend UI pages for you! Follow these easy steps:

### Step 1: Clone the repository
Make sure you have Git installed, then run:
```bash
git clone https://github.com/ArionGD/User-Friendly-System-Call-Interface-for-Enhanced-Security-ADI.git
cd User-Friendly-System-Call-Interface-for-Enhanced-Security-ADI
```

### Step 2: Set up a virtual environment (Recommended)
This prevents project dependencies from interfering with your global Python setup.
* **On Windows:**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
* **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install dependencies
Install all the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 4: Start the Flask application
Navigate to the `backend` folder and start the server:
```bash
cd backend
python app.py
```

### Step 5: Open it in your browser
Once the backend server starts, open your web browser and go to:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 📦 Dependencies Explained

Here are the key tools this project uses and why they are necessary:

* **Flask**: The core Python framework that powers our backend APIs and hosts the frontend website.
* **Flask-CORS**: Enables Cross-Origin Resource Sharing so our frontend and backend can exchange data without security blocks during local development.
* **PyJWT**: Generates and validates JSON Web Tokens so users can securely log in and stay authenticated.
* **bcrypt**: Safely hashes and encrypts user passwords before they get stored in the database.
* **python-dotenv**: Automatically loads secret settings (like DB paths) from a `.env` file.
* **cryptography**: Handles AES-256 file encryption and decryption routines.

📁 What’s Inside: Modules & Features

| Module / Component                   | Responsibilities / Features                                                                                                     |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **Authentication & Auth Layer**      | Secure login, token-based sessions, role-based access control (RBAC)                                                            |
| **Protected System Call Interface**  | Safe wrappers for file operations, process/network calls; input sanitization; permission enforcement                            |
| **File Manager + Encryption**        | Upload / Download / Edit / Delete / Recycle-Bin for files, AES-256 encryption support, optional file passcode locking           |
| **Audit Logging**                    | Detailed logging of every action — user, timestamp, operation, parameters, status, IP/client info                               |
| **Security Dashboard / Admin Panel** | Stats & metrics: total files, encrypted files, active users, unauthorized attempts; real-time logs; system-call activity charts |
| **Future-ready hooks**               | Designed for optional modules like anomaly detection, MFA, firewall / rate-limiting, version history, alerts                    |


💡 Key Features

🔐 Secure Authentication — login with tokens, role-based permission; separation between admin and normal users.

🗄️ Advanced File Management — upload, edit, download, delete; encrypted storage; file-level locking and recycle bin with restore.

⚙️ Controlled System Calls — OS-level operations executed only through validated, sanitized requests.

📜 Full Audit Logs — every system call and user action logged with details (user, time, parameters, result).

📊 Admin Dashboard — view system activity, file stats, unauthorized attempts, real-time logs, and activity graphs.


🛠️ Tech Stack
Layer	Technologies / Tools
Frontend	HTML, CSS, JavaScript (modern UI)
Backend	Python (Flask / FastAPI)
System Layer	C or system-level wrappers (for low-level calls) + Python bridging
Security	JWT authentication, AES-256 encryption, Role-Based Access Control (RBAC)
Storage / Logs	SQLite or secure flat-file / database
Dependencies	See requirements.txt


🧱 Project Structure
```
/
├── backend/           # API server, authentication, syscall interface
├── frontend/          # Web UI (file manager, dashboard)
├── database/          # DB or storage setup
├── docs/              # Documentation, design notes
├── README.md          # ← You are here
└── requirements.txt   # Python (and other) dependencies
```


🧭 How to Use the System

### 1. Account Setup
Since this is running locally, you can create a fresh account on the signup page.
* You can choose your role during sign-up: `admin`, `user`, or `viewer`.
* An **Admin** gets access to full logs, dashboards, and unrestricted system/file commands.
* A **User** can perform secure file management.
* A **Viewer** has read-only system permissions.

### 2. Admin Dashboard
Log in with an account registered as an `admin` to access the Dashboard:
* View total system statistics and active sessions.
* Check real-time audit logs of every system call.
* Monitor failed or unauthorized access attempts.

### 3. File Manager & Encryption
* Upload files to the secure storage interface.
* Use the AES-256 locking mechanism to encrypt critical files with a password.


🧑‍💻 How to Contribute

Contributions, improvements, bug-fixes, and documentation enhancements are welcome!

Fork the repository

Create a new branch (git checkout -b feature/my-feature)

Make changes & add tests as needed

Submit a Pull Request — please describe your changes and rationale


📄 License

This project is licensed under the MIT License. See the LICENSE
 file for details.


🙋 Author / Maintainer

rajaman85, sushantranjan912, bittusingh14 — we’re the original authors. Thanks for building and sharing this!


🔮 Future Roadmap & Enhancements

🛡️ Multi-Factor Authentication (MFA)

🤖 ML-based Anomaly Detection & Alerting for suspicious usage patterns

🔔 Real-time Alerts (email / SMS) for security events

📂 Version history for files

🛑 Firewall / Rate-limiting on system calls

🔄 More OS-level operations (network, process management, etc.)

“A well-documented project is the first step toward collaboration and trust.”

Thanks for checking out this project — feel free to ⭐ the repo if you like it!
