from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home_redirects():
    r = client.get("/", allow_redirects=False)
    assert r.status_code in (302, 303)
