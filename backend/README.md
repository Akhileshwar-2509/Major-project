Backend (FastAPI)

Setup

- Install Poetry
- cd backend
- poetry install
- cp .env.example .env
- poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

API Endpoints

- POST /predict/yield
- POST /recommend/cover
- POST /classify/weed
- POST /optimize/fertilizer
- POST /explain/why

