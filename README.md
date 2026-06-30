## 🧭 Installation & Usage

Follow these steps carefully to set up and run the project locally.

---

# ✅ Prerequisites

Make sure the following are installed on your system:

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

Run:

```bash
pip install -r requirements.txt
```

This installs all required Python packages and dependencies needed for the backend server.

> If pip is outdated, update it using:

```bash
python -m pip install --upgrade pip
```

---

# ⚙️ Step 4: Configure the Project (Optional)

You may configure:

* Encryption keys
* Database paths
* Role permissions
* Security settings

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
