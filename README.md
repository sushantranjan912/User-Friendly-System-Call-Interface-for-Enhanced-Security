🚀 Secure System Call Interface (Enhanced Security File Manager)

A modern web-based system designed to securely execute system-level operations, manage files, monitor real-time logs, and enforce access control using a layered security architecture.

🔥 Key Features
🔐 Secure Authentication

Login with token-based security

AppLock (file-level passcode protection)

Safe user session handling

🛡 Authorization (RBAC)

Role-based access control

Permissions: View, Download, Edit, Delete

Admin vs Normal User privilege separation

⚙️ Protected System Call Interface

Safe execution of OS-level operations

Input validation & sanitization

Prevents unauthorized or harmful system calls

📁 Advanced File Manager

Upload, View, Edit, Download, Delete

AES-256 Encryption support

Locked files with passcode

File metadata display

🗑 Recycle Bin

Deleted files stored temporarily

30-minute countdown before permanent deletion

Restore / Delete Forever options

📊 Security Dashboard

Total Files

Encrypted Files

Active Users

Unauthorized Actions

System Call Activity Graph

File Security Snapshot (100% Secure)

🧾 Audit Logs (Real-Time)

Logs file uploads, deletions, edits, downloads

Tracks login events

Shows IP address, timestamp, status, details

Export logs for analysis

🛠 Tech Stack
Frontend

HTML, CSS, JavaScript

Modern dark UI

Backend

Python (Flask API)

C (Low-level system call layer)

Security

JWT Authentication

AES-256 Encryption

RBAC Permission Model

AppLock File Protection

Database / Storage

SQLite or secure flat-file logging

📁 Project Modules
1. Authentication Module

Validates login

Generates secure tokens

2. Authorization & Security

Role-based access

Permission enforcement

3. System Call Interface

Validates syscall request

Executes safely using C/Python

4. File Manager

Upload/Edit/Delete/Download

Encryption & Locking

5. Recycle Bin

Temporary storage

Auto-expiry countdown

6. Audit Logging

Tracks all system activities

Helps in monitoring & debugging

🔮 Future Enhancements

Multi-Factor Authentication (MFA)

AI-based anomaly detection

Email/SMS alerts for suspicious activity

Version history for each file

Advanced firewall & rate limiting
