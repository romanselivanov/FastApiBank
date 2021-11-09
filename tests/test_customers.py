from main import app
from fastapi.testclient import TestClient


def test_sign_up(temp_db):
    request_data = {
        "first_name": "john",
        "last_name": "dow",
        "patronymic": "dowich",
        "email": "dow@ex.com",
        "phone": "555555",
        "password": "TestPass340"
    }
    with TestClient(app) as client:
        response = client.post("/sign-up", json=request_data)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == "dow@ex.com"
    assert response.json()["first_name"] == "john"
    assert response.json()["token"] is not None


def test_login(temp_db):
    request_data = {"username": "dow@ex.com", "password": "TestPass340"}
    with TestClient(app) as client:
        response = client.post("/login", data=request_data)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None


def test_login_with_invalid_password(temp_db):
    request_data = {"username": "dow@ex.com", "password": "unicorn"}
    with TestClient(app) as client:
        response = client.post("/login", data=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


def test_user_detail_forbidden_without_token(temp_db):
    with TestClient(app) as client:
        response = client.get("/me")
    assert response.status_code == 401


# def test_user_detail(temp_db):
#     with TestClient(app) as client:
#         # Create user token to see user info
#         loop = asyncio.get_event_loop()
#         token = loop.run_until_complete(create_user_token(user_id=1))
#         response = client.get(
#             "/me",
#             headers={"Authorization": f"Bearer {token['token']}"}
#         )
#     assert response.status_code == 200
#     assert response.json()["id"] == 1
#     assert response.json()["email"] == "vader@deathstar.com"
#     assert response.json()["name"] == "Darth"