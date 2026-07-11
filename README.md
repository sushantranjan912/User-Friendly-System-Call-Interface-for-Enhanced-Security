## 🧭 Installation & Usage

Follow these steps carefully to set up and run the project locally.

---

# ✅ Prerequisites

Make sure the following are installed on your system:


**Why this project matters:**
* Python 3.10 or above
* Git
* A code editor like VS Code

You can verify installation using:

```bash
python --version
git --version
```

---

# 📥 Step 1: Clone the Repository

Open terminal or command prompt and run:

```bash
git clone https://github.com/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security.git
```

This downloads the project to your computer.

Now move into the project folder:

```bash
cd User-Friendly-System-Call-Interface-for-Enhanced-Security
```

---

# 🛠️ Step 2: Create Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

After activation, you should see `(venv)` in the terminal.

---

# 📦 Step 3: Install Dependencies

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

based on your requirements.

---

# 🚀 Step 5: Run the Backend Server

Move into backend directory:

```bash
cd backend
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

If successful, you will see output similar to:

```bash
Uvicorn running on http://127.0.0.1:8000
```

The backend server is now running locally.

---

# 🌐 Step 6: Launch Frontend

Open the frontend files in your browser.

You can either:

* Open `frontend/index.html` directly
  OR
* Run a frontend development server if configured

---

# 🔑 Step 7: Login & Use Features

After launching the project:

* Login using user/admin credentials
* Upload and manage files
* View logs and activity
* Access dashboard features based on your role

---

# 📊 Admin Dashboard

Admins can:

* Monitor system activity
* View audit logs
* Check unauthorized access attempts
* Analyze file and user statistics

---

# ❗ Common Beginner Issues

## `uvicorn` not recognized

Install uvicorn manually:

```bash
pip install uvicorn
```

---

## Permission denied while activating virtual environment

Try running terminal as administrator or use the correct activation command for your OS.

---

## Missing dependencies

Run again:

```bash
pip install -r requirements.txt
```

---

# ✅ Project Successfully Running

If everything works correctly:

* Backend runs on localhost
* Frontend opens successfully
* Login system works
* Dashboard and file manager become accessible
