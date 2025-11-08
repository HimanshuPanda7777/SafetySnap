# SafetySnap
PPE (personal protective equipment) detection app to identify helmets, gloves, and vests from images, ensuring workplace safety compliance.
# SafetySnap (React + FastAPI)

## Run Backend

```bash
cd backend
python -m venv .venv
# Activate venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

## Run Frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs at **[http://localhost:3000](http://localhost:3000)**

## Run Both Together (optional)

In `frontend/package.json`:

```json
"scripts": {
  "start": "react-scripts start",
  "server": "cd ../backend && uvicorn main:app --reload",
  "dev": "concurrently \"npm run server\" \"npm start\""
}
```

Then run:

```bash
npm run dev
```

✅ **Summary:**

* Backend → FastAPI via `uvicorn main:app --reload`
* Frontend → React via `npm start`
* Both → `npm run dev`

