import pytest
from fastapi.testclient import TestClient

# from token_config import TOKEN

from ..main import app

# Create a test client for the FastAPI app
client = TestClient(app)

def get_token():
    user_credentials = {"email": "admin@gmail.com", "password": "mypassword"}
    response = client.post("/v1/auth", json=user_credentials)
    return response.json()['token']

def test_authenticate_user():
    # Test case 1: Valid user credentials
    user_credentials = {"email": "admin@gmail.com", "password": "mypassword"}
    response = client.post("/v1/auth", json=user_credentials)
    assert response.status_code == 200
    assert response.json()["token"] is not None

    # Test case 2: Invalid email credentials
    user_credentials = {
        "email": "invaliduser@example.com",
        "password": "invalidpassword",
    }
    domain_name = user_credentials["email"].split("@")[1]
    response = client.post("/v1/auth", json=user_credentials)
    assert response.status_code == 422
    assert (
        response.json()["detail"]
        == f"The domain name {domain_name} does not accept email."
    )

    # Test case 3: Invalid user credentials
    user_credentials = {"email": "invaliduser@email.com", "password": "invalidpassword"}
    response = client.post("/v1/auth", json=user_credentials)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

    # Test case 4: Invalid email and password credentials
    user_credentials = {"email": "invaliduseremail.com", "password": "invalidpassword"}
    response = client.post("/v1/auth", json=user_credentials)
    assert response.status_code == 422
    assert (
        response.json()["detail"]
        == "The email address is not valid. It must have exactly one @-sign."
    )


# test cases for temp recommender api
def test_temp_recommender():
    # Test Case 1: invalid parameters
    params = {
        "city": "valid_city_id_with_36_characters",
        "state": "valid_state_id_with_36_characters",
        "speciality": "valid_speciality_id_with_36_chars",
        "certificate": "valid_certificate_id_with_36_chars",
    }
    headers = {"Authorization": "invalid_token"}
    response = client.get("/v1/recommend-temp", headers=headers, params=params)
    assert response.status_code == 422
    details = response.json()["detail"]
    assert any("string_too_short" in d["type"] for d in details)

    # Test Case 2: valid parameters and token
    params = {
        "city": "e9b9a7f2-f5c9-4a8c-a4a1-5c3a9b8d9f2b",
        "state": "1a6ea7c1-d8c0-4f9e-b7d4-a5c7e8d6b2e4",
        "speciality": "7b4f9d8e-f1b2-4c6d-9a3d-6c1e5b7a9d7f",
        "certificate": "3c8f6b8a-8e9e-4b5c-bc8d-c9f7e2d1f3a6",
    }
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/v1/recommend-temp", headers=headers, params=params)
    assert response.status_code == 200
    assert len(response.json()["data"]["temps"]) == 5

    # Test Case 3: valid parameters but invalid token
    params = {
        "city": "e9b9a7f2-f5c9-4a8c-a4a1-5c3a9b8d9f2b",
        "state": "1a6ea7c1-d8c0-4f9e-b7d4-a5c7e8d6b2e4",
        "speciality": "7b4f9d8e-f1b2-4c6d-9a3d-6c1e5b7a9d7f",
        "certificate": "3c8f6b8a-8e9e-4b5c-bc8d-c9f7e2d1f3a6",
    }
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/v1/recommend-temp", headers=headers, params=params)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

    # Test Case 4: valid parameters but no token
    params = {
        "city": "e9b9a7f2-f5c9-4a8c-a4a1-5c3a9b8d9f2b",
        "state": "1a6ea7c1-d8c0-4f9e-b7d4-a5c7e8d6b2e4",
        "speciality": "7b4f9d8e-f1b2-4c6d-9a3d-6c1e5b7a9d7f",
        "certificate": "3c8f6b8a-8e9e-4b5c-bc8d-c9f7e2d1f3a6",
    }
    response = client.get("/v1/recommend-temp", params=params)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["header", "authorization"]


# test cases for shift recommender api
def test_shift_recommender():

    # Test case 1: Valid request
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "city": "e9b9a7f2-f5c9-4a8c-a4a1-5c3a9b8d9f2b",
        "state": "1a6ea7c1-d8c0-4f9e-b7d4-a5c7e8d6b2e4",
        "speciality": "7b4f9d8e-f1b2-4c6d-9a3d-6c1e5b7a9d7f",
        "certificate": "3c8f6b8a-8e9e-4b5c-bc8d-c9f7e2d1f3a6",
    }
    response = client.get("/v1/recommend-shifts", headers=headers, params=params)
    assert response.status_code == 200
    assert len(response.json()['data']['shift']) == 5

