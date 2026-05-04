Before Running:
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy pytest
JWT: pip install "python-jose[cryptography]"

Running Command:
    uvicorn app.main:app --reload

Swagger WebSite:
    http://127.0.0.1:8000/docs