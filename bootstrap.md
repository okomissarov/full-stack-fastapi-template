# Bootstrap: Full Stack FastAPI Template (No Docker)

## Your Task

Install all dependencies and prepare the local development environment for the Full Stack FastAPI Template. This runs everything natively — no Docker required.

---

## Prerequisites

The following tools are needed. Install any that are missing.

### 1. Python 3.10+

```bash
python3 --version
```

If missing: `sudo apt-get install -y python3 python3-pip`

### 2. uv (Python package manager)

```bash
uv --version
```

If missing:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Node.js 18+ and npm

```bash
node --version && npm --version
```

If missing: `sudo apt-get install -y nodejs npm`

### 4. PostgreSQL 14+

```bash
psql --version
```

If missing:
```bash
sudo apt-get update -qq
sudo apt-get install -y postgresql postgresql-client
```

---

## Setup Steps

### Step 1: Start PostgreSQL and Create Database

```bash
sudo systemctl start postgresql

# Create database and set password (matches .env defaults)
sudo -u postgres psql -c "CREATE DATABASE app;"
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'changethis';"
```

### Step 2: Install Backend Dependencies

```bash
cd backend
uv sync
```

### Step 3: Run Database Migrations and Seed Data

```bash
cd backend
uv run alembic upgrade head
uv run python app/initial_data.py
```

### Step 4: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 5: Start the App

From the project root:

```bash
bash scripts/start.sh
```

### Step 6: Verify

| Service        | URL                        |
|----------------|----------------------------|
| Frontend       | http://localhost:5173       |
| Backend API    | http://localhost:8000       |
| Swagger Docs   | http://localhost:8000/docs  |

Login: `admin@example.com` / `changethis`

---

## Stop the App

```bash
bash scripts/stop.sh
```

---

## Troubleshooting

**PostgreSQL won't start:**
```bash
sudo systemctl status postgresql
sudo journalctl -u postgresql --no-pager -n 20
```

**Port already in use:**
```bash
# Check what's using the port
lsof -i :5173
lsof -i :8000
# Kill it
kill $(lsof -t -i:5173) 2>/dev/null
```

**Backend can't connect to database:**
- Verify PostgreSQL is running: `pg_isready`
- Check `.env` values match your PostgreSQL setup
- Ensure `pg_hba.conf` allows password auth for localhost connections

**Migrations fail:**
- Ensure database `app` exists: `sudo -u postgres psql -c "\l"`
- Check `.env` has correct `POSTGRES_*` values
