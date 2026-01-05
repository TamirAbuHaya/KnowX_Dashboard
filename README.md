# 🚀 Django API + Vite SPA Dashboard

A modern **full-stack dashboard** with a clean separation of concerns:

- 🧠 **Backend:** Django + Django REST Framework (API only)
- ⚡ **Frontend:** Vite + React + TypeScript (Single Page Application)

The frontend runs on a Vite development server and **proxies API calls** to the Django backend during development.

---

## 📁 Project Structure

```
myproject/
├── backend/     # Django API
├── frontend/    # Vite + React SPA
└── README.md
```

---

## 🧩 Prerequisites

Make sure the following are installed **before starting**:

### ✅ Required
- **Python 3.10+** (recommended: 3.11)
- **Node.js LTS** (includes npm)
- (Optional but recommended) **Git**

### 🔍 Verify installations

```powershell
python --version
pip --version
node -v
npm -v
```

---

## 🐍 Backend Setup (Django API)

📍 Open a **PowerShell** window:

### 1️⃣ Navigate to backend
```powershell
cd backend
```

### 2️⃣ Create & activate virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3️⃣ Install backend dependencies
```powershell
pip install -r requirements.txt
```

### 4️⃣ Run database migrations
```powershell
python manage.py migrate
```

### 5️⃣ Start the Django server
```powershell
python manage.py runserver 127.0.0.1:8000
```

✅ Backend is now running at:
- http://127.0.0.1:8000

🩺 Health check (if enabled):
- http://127.0.0.1:8000/api/health/

---

## ⚡ Frontend Setup (Vite + React + TypeScript)

📍 Open a **second PowerShell window**:

### 1️⃣ Navigate to frontend
```powershell
cd frontend
```

### 2️⃣ Install frontend dependencies
```powershell
npm install
```

### 3️⃣ Start the Vite dev server
```powershell
npm run dev
```

✅ Frontend is now running at:
- http://localhost:5173

---

## 🔗 API Proxy (Development)

During development, Vite automatically proxies requests:

| Frontend Path | Proxied To |
|---------------|------------|
| `/api/*` | `http://127.0.0.1:8000/api/*` |
| `/media/*` | `http://127.0.0.1:8000/media/*` |

✔️ This avoids CORS issues and allows cookie-based authentication.

---

## 🔄 Daily Development Workflow

🟢 **Terminal 1 – Backend**
```powershell
cd backend
.\.venv\Scripts\activate
python manage.py runserver 127.0.0.1:8000
```

🟢 **Terminal 2 – Frontend**
```powershell
cd frontend
npm run dev
```

You’re now ready to develop 🎉

---

## 🛠️ Common Issues & Fixes

### ❌ `node` or `npm` not recognized
➡️ Install **Node.js LTS** from:
https://nodejs.org  
Then restart PowerShell.

---

### ❌ PowerShell blocks npm (`npm.ps1 cannot be loaded`)
Run **once** (safe, current user only):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

### ❌ `Backend health: error` / `ECONNREFUSED 127.0.0.1:8000`
Cause: Django is not running or is using a different port.

✔️ Fix:
```powershell
python manage.py runserver 127.0.0.1:8000
```

If you changed the port, update the proxy in:
```
frontend/vite.config.ts
```

---

## 🔐 Security Notes

- 🔒 All authentication, roles, and permissions are enforced **server-side** in Django
- 👀 The frontend controls UI visibility only — never security
- 📁 File access and review logic always live in the backend

---

---

Happy coding 🚀
