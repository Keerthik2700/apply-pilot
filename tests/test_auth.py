import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_login_flow():
    # Note: In full CI, you'd use a test DB. This smoke test checks route existence.
    resp = client.get("/login")
    assert resp.status_code == 200
