# build4better-hackathon-codesphere-3.0
A repository for our project for Build4Better hackathon in CodeSphere 3.0. Team: Black Mesa (myself, Barira Waris, and Naveed Zahir).

---

## Deployments and Database
Frontend: https://backend-blackmesa-build4better.onrender.com
Backend: https://frontend-blackmesa-build4better.onrender.com
Database: https://supabase.com/dashboard/project/dtdcmsncaftksemvbxjr

## Quickstart & Initialization Guide

Follow the steps below to set up and run both the backend and frontend on your local machine.

### Prerequisites
* **Python: `3.12.7` is strictly required** (compulsory to avoid dependency version conflicts or wheel build issues).
* **Node.js:** `v20.x` or higher and `npm`.
* **Git**

---

### 1. Clone the Repository
```bash
git clone https://github.com/OwaisAhmedKhan64/build4better-hackathon-codesphere-3.0.git
cd build4better-hackathon-codesphere-3.0
```

---

### 2. Backend Setup (FastAPI + Supabase)

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment (using Python 3.12.7):**
   * **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   * **macOS / Linux:**
     ```bash
     python3.12 -m venv .venv
     source .venv/bin/activate
     ```

     Check through `python --version` in terminal.

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables:**
   Copy the `.env.example` file to create your `.env`:
   * **Windows:**
     ```powershell
     copy .env.example .env
     ```
   * **macOS / Linux:**
     ```bash
     cp .env.example .env
     ```
   Fill in your Supabase credentials in `backend/.env`:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_PUBLISHABLE_KEY=your-anon-key
   SUPABASE_SECRET_KEY=your-service-role-or-secret-key
   FRONTEND_URL=http://localhost:5173
   ```

5. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   * API root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   * Interactive OpenAPI / Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 3. Frontend Setup (Vue 3 + Tailwind v4 + Pinia + Vue Router)

1. **Open a new terminal and navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up Environment Variables:**
   * **Windows:**
     ```powershell
     copy .env.example .env
     ```
   * **macOS / Linux:**
     ```bash
     cp .env.example .env
     ```
   Ensure `frontend/.env` points to your backend:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Start the frontend development server:**
   ```bash
   npm run dev
   ```
   * Web App: [http://localhost:5173](http://localhost:5173)

---

### 4. Verifying System Health
Once both servers are running:
1. Open [http://localhost:5173](http://localhost:5173).
2. Click the **"System Status"** button in the top navbar or the floating badge at the bottom right.
3. The diagnostics modal will verify:
   * **FastAPI:** Live HTTP heartbeat.
   * **Supabase:** Live database query & row insertion test.

---

### Project Architecture Overview

```text
build4better-hackathon-codesphere-3.0/
├── backend/
│   ├── app/
│   │   ├── core/config.py     # Centralized settings & dynamic CORS
│   │   ├── routers/           # Modular endpoint routes (system, notes, etc.)
│   │   ├── schemas/           # Pydantic data validation schemas
│   │   ├── db.py              # Supabase connection client
│   │   └── main.py            # FastAPI application entrypoint
│   ├── Procfile               # Cloud deployment start command
│   ├── requirements.txt       # Dependencies (Python 3.12.7)
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── api/client.ts      # Axios instance
    │   ├── components/        # Navbar & System Health diagnostics
    │   ├── router/index.ts    # Vue Router configuration
    │   ├── stores/            # Pinia global state
    │   ├── types/index.ts     # TypeScript interfaces
    │   ├── views/             # HomeView, DashboardView
    │   ├── App.vue            # Global layout shell
    │   └── main.ts            # Vue bootstrap
    ├── vite.config.ts         # Vite + Tailwind v4 + @ alias
    └── .env.example
```
