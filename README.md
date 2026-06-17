![GitHub forks](https://img.shields.io/github/forks/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security?style=for-the-badge)
![GitHub Repo stars](https://img.shields.io/github/stars/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security?style=for-the-badge&color=white)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security?style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security?style=for-the-badge)


# 🛡️ User-Friendly System Call Interface for Enhanced Security

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

# 🔎 About the project

Secure System Call Interface (Enhanced Security File Manager) is a web-based platform designed to **perform system-level operations safely** (like file management and process execution) via a controlled interface — with **authentication, role-based authorization, encryption, and comprehensive logging**.  
It acts as a “gateway” for system calls, ensuring unauthorized or malicious operations are prevented, and all activity is auditable.

**Why this project matters:**

- Most native system calls expose powerful operations — misuse could compromise the system.  
- This interface restricts those operations to authorized users only.  
- Detailed logs + audit trails + optional analytics help administrators monitor usage and detect suspicious behavior.  



# 🚀  Quick Start

1. Clone the repository
```bash
git clone https://github.com/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security.git
cd User-Friendly-System-Call-Interface-for-Enhanced-Security
```
2. Setup virtual environment (for backend)
```sh
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. Install dependencies
```sh
pip install -r requirements.txt
```

4. Run the backend
```sh
cd backend
uvicorn main:app --reload
```

5. Open frontend in browser
```txt
# (Open index.html or as per frontend docs; or start frontend server if configured)
```


# 📁 What’s Inside: Modules & Features

| | Module / Component                   | Responsibilities & Features                                                                                                     |
|---| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| 🔐| **Authentication & Auth Layer**      | Secure login, token-based sessions, role-based access control (RBAC)                                                            |
| 🛡️| **Protected System Call Interface**  | Safe wrappers for file operations, process/network calls; input sanitization; permission enforcement                            |
| 🗄️ | **File Manager + Encryption**        | Upload / Download / Edit / Delete / Recycle-Bin for files, AES-256 encryption support, optional file passcode locking           |
|📜| **Audit Logging**                    | Detailed logging of every action — user, timestamp, operation, parameters, status, IP/client info                               |
| ⚙️|**Security Dashboard / Admin Panel** | Stats & metrics: total files, encrypted files, active users, unauthorized attempts; real-time logs; system-call activity charts |
|📁| **Future-ready hooks**               | Designed for optional modules like anomaly detection, MFA, firewall / rate-limiting, version history, alerts                    |


# 💡 Key Features

 🔐 Secure Authentication — login with tokens, role-based permission; separation between admin and normal users.

🗄️ Advanced File Management — upload, edit, download, delete; encrypted storage; file-level locking and recycle bin with restore.

⚙️ Controlled System Calls — OS-level operations executed only through validated, sanitized requests.

📜 Full Audit Logs — every system call and user action logged with details (user, time, parameters, result).

📊 Admin Dashboard — view system activity, file stats, unauthorized attempts, real-time logs, and activity graphs.


# Build with
![Static Badge](https://img.shields.io/badge/Html-grey?style=for-the-badge&logo=html5&logoColor=orange&logoSize=auto&labelColor=white)
![Static Badge](https://img.shields.io/badge/CSS-blue?style=for-the-badge&logo=css&logoColor=blue&logoSize=auto&labelColor=white)
![Static Badge](https://img.shields.io/badge/javascript-grey?style=for-the-badge&logo=javascript&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Flask%2FFastapi-silver?style=for-the-badge&logo=flask&logoColor=white&logoSize=auto&labelColor=grey)
![Static Badge](https://img.shields.io/badge/SQLite-cyan?style=for-the-badge&logo=sqlite&logoColor=white&logoSize=auto&labelColor=grey)
![Static Badge](https://img.shields.io/badge/Python-white?style=for-the-badge&logo=python&logoColor=blue&logoSize=auto)

---

# 🛠️ Tech Stack

 - Layer	Technologies / Tools
 - Frontend	HTML, CSS, JavaScript (modern UI)
 - Backend	Python (Flask / FastAPI)
 - System Layer	C or system-level wrappers (for low-level calls) + Python bridging
 - Security	JWT authentication, AES-256 encryption, Role-Based Access Control (RBAC)
 - Storage / Logs	SQLite or secure flat-file / database
 - Dependencies	See requirements.txt


# 🧱 Project Structure

```
/
├── backend/           # API server, authentication, syscall interface
├── frontend/          # Web UI (file manager, dashboard)
├── database/          # DB or storage setup
├── docs/              # Documentation, design notes
├── README.md          # ← You are here
└── requirements.txt   # Python (and other) dependencies
```


# Getting Started

Getting started with this repo is simple. choose the best setup environment for you to start.
here we recommend you to follow the below steps
🧭 Installation & Usage

1.Clone & setup
```sh
git clone https://github.com/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security.git
cd User-Friendly-System-Call-Interface-for-Enhanced-Security
```

3.
    ```sh
     cd User-Friendly-System-Call-Interface-for-Enhanced-Security
   ```
5. For  Activating and Running the Environment
  ```sh
source venv/bin/activate
python -m venv venv
```

5. pip install -r requirements.txt


6. Configure settings

(Optional) Update configuration — e.g., encryption keys, database path, role permissions, etc.

7. Run the backend API

```sh cd backend
uvicorn main:app --reload
```

8. Launch frontend

- Either open frontend/index.html in browser or start frontend development server (if configured).

- Admin or user login, then perform permitted operations (file upload / download / view logs) as per your role.

- Admin Dashboard

- Use admin credentials to view dashboard: system logs, file stats, unauthorized attempts, activity graphs, etc.



# 🧑‍💻 contributing
---
1.There are many ways you can contribute to User-Friendly-System-Call-Interface-for-Enhanced-Security:

 - Report bugs or submit features.
 - review the documentation and submit pull request to improve it wheather it's fixing typos or adding new content.
 - Talk or write about thid repo.
 - show your support for upgrading new features.

2. Contributions, improvements, bug-fixes, and documentation enhancements are welcome!

3. Fork the repository

4. Create a new branch (git checkout -b feature/my-feature)
5. Open  a Pull Request — please describe your changes and rationale


📄 License

This project is licensed under the MIT License. See the LICENSE
 file for details.


# 🙋 Author / Maintainer

rajaman85, sushantranjan912, bittusingh14 — we’re the original authors. Thanks for building and sharing this!

# Features
🔮 Future Roadmap & Enhancements

🛡️ Multi-Factor Authentication (MFA)

🤖 ML-based Anomaly Detection & Alerting for suspicious usage patterns

🔔 Real-time Alerts (email / SMS) for security events

📂 Version history for files

🛑 Firewall / Rate-limiting on system calls

🔄 More OS-level operations (network, process management, etc.)

“A well-documented project is the first step toward collaboration and trust.”

Thanks for checking out this project — feel free to ⭐ the repo if you like it!

## Acknowledgements

Thanks to these wonderful people who contributed to this repository:

<!-- ALL-CONTRIBUTORS-LIST:START -->

| [@sushantranjan912](https://github.com/sushantranjan912) | [rajaman85](https://github.com/rajaman85) |
| :---: | :---: |
| 💻 📖 | 💻 🚇 |
<!-- ALL-CONTRIBUTORS-LIST:END -->


