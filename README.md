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

## 🚀 Demo / Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security.git
cd User-Friendly-System-Call-Interface-for-Enhanced-Security

# 2. Setup virtual environment (for backend)
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the backend
cd backend
uvicorn main:app --reload

# 5. Open frontend in browser
# (Open index.html or as per frontend docs; or start frontend server if configured)
```


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

## Project structure

```text
User-Friendly-System-Call-Interface-for-Enhanced-Security/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── database/
│   ├── routes/
│   ├── utils/
│   └── ssci_files/
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── pages/
├── database/
├── docs/
└── requirements.txt
```

---

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer
- `pip`
- A browser like Chrome, Edge, or Firefox

---

## Local setup instructions

### 1) Clone the repository

```bash
git clone https://github.com/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security.git
cd User-Friendly-System-Call-Interface-for-Enhanced-Security
```

### 2) Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Install the Python dependencies

The dependency file is in the project root.

```bash
pip install -r requirements.txt
```

### 4) Optional: configure environment variables

The app reads values from a `.env` file through `python-dotenv`.

You can create a `.env` file inside `backend/` and add values like these:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_PATH=database/database.db
ENCRYPTION_KEY=your-fernet-key
```

If you skip this step, the project uses development defaults, but custom values are better for real use.

### 5) Run the backend server

Go into the backend folder and start Flask directly.

```bash
cd backend
python app.py
```

On Windows, if `python` does not work, try:

```bash
py app.py
```

### 6) Open the app in your browser

Visit:

```text
http://localhost:5000
```

The Flask server serves the frontend from the same address, so there is no separate frontend startup command.

---

## Correct runtime command

This project uses **Flask**, not FastAPI.

So the correct command is:

```bash
python app.py
```

Not:

```bash
uvicorn main:app --reload
```

---

## How to use the app

### For a normal user
- register or log in
- upload or manage allowed files
- run only permitted system commands
- view personal logs and history
- restore deleted files from the recycle bin if allowed

### For an admin
- manage users and view broader system activity
- see audit logs and security events
- monitor file actions and command history
- review unauthorized or failed actions

### For a viewer
- access only limited read-only actions
- no edit or destructive permissions

---

## Dependencies explained

### Flask
Flask is the web framework used to build the backend server and API routes.

### Flask-CORS
This helps the frontend talk to the backend during local development.

### PyJWT
Used to create and verify login tokens after authentication.

### bcrypt
Used to hash passwords safely before storing them in the database.

### python-dotenv
Loads values from a `.env` file so secret settings do not have to be hard-coded.

### cryptography
Used here for secure encryption and decryption of sensitive log details.

---

## Main API areas

The backend is organized into separate routes for clarity:

- **`/api/auth`** → register, login, logout
- **`/api/system`** → approved system command execution and history
- **`/api/files`** → file manager actions
- **`/api/recycle-bin`** → restore or permanently delete removed files
- **`/api/logs`** → audit logs and log statistics

---

## How to test

1. Open the project in your editor and check that `README.md` has clear setup steps.
2. Create and activate the virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Run the backend using `python app.py` from the `backend` folder.
5. Open `http://localhost:5000` in your browser.
6. Check that the frontend loads and the API responds normally.

You can also test the API by opening:

```text
http://localhost:5000/api/test
```

---


Configure settings

(Optional) Update configuration — e.g., encryption keys, database path, role permissions, etc.

Run the backend API

cd backend
uvicorn main:app --reload


Launch frontend

Either open frontend/index.html in browser or start frontend development server (if configured).

Admin or user login, then perform permitted operations (file upload / download / view logs) as per your role.

Admin Dashboard

Use admin credentials to view dashboard: system logs, file stats, unauthorized attempts, activity graphs, etc.


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
