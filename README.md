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

## 🚀 Getting Started

### Installation & Setup

Follow these simple steps to get the project running locally:

**1. Clone the repository**
```bash
git clone https://github.com/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security.git
cd User-Friendly-System-Call-Interface-for-Enhanced-Security
```

**2. Set up a virtual environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r backend/requirements.txt
```

**4. Start the Flask backend server**
```bash
cd backend
python app.py
```
The backend will start on `http://localhost:5000`

**5. Open the frontend in your browser**
```
http://localhost:5000
```

### Dependencies Explained

Here's what each key dependency does:

- **Flask** — Web framework that handles HTTP requests and serves the frontend interface
- **PyJWT** — Securely creates and validates authentication tokens for login sessions
- **bcrypt** — Hashes and validates user passwords securely (never stores plain text)
- **python-dotenv** — Loads environment variables from `.env` file for sensitive configuration
- **cryptography** — Provides AES-256 encryption for protecting sensitive files

### User Roles & Dashboard

- **Admin User** — Full access to file management, system calls, and admin dashboard with logs and statistics
- **Regular User** — Can upload, download, and manage their own files; can view their activity logs
- **Admin Dashboard** — Shows system statistics, file activity, unauthorized access attempts, and real-time logs


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
Backend	Python (Flask)
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


‍💻 How to Contribute

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
