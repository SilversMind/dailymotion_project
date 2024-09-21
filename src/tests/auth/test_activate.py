import base64
import pytest
from fastapi.testclient import TestClient
from src.auth.database import save_user, UserRegistration, activate_user

@pytest.fixture
def user_data():
    return {
        "email": "johndoe@example.com",
        "password": "azertyuiop",
        "activation_code": "1234"
    }

@pytest.fixture
def encoded_credentials(user_data):
    return base64.b64encode(f"{user_data['email']}:{user_data['password']}".encode()).decode()

def setup_user(get_test_db, get_test_cache, user_data):
    save_user(UserRegistration(email=user_data["email"], password=user_data["password"]), get_test_db)
    get_test_cache.set(user_data["email"], user_data["activation_code"])

def test_activate_account_success(client: TestClient, get_test_db, get_test_cache, user_data, encoded_credentials) -> None:
    setup_user(get_test_db, get_test_cache, user_data)

    data = {"activation_code": user_data["activation_code"]}
    response = client.post("/activate", json=data, headers={"Authorization": f"Basic {encoded_credentials}"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "Account sucessfully activated"

def test_activate_account_user_not_found(client: TestClient, user_data, encoded_credentials) -> None:
    data = {"activation_code": user_data["activation_code"]}
    response = client.post("/activate", json=data, headers={"Authorization": f"Basic {encoded_credentials}"})
    
    assert response.status_code == 404
    assert response.json()["detail"] == "This account is not registered"

def test_activate_account_incorrect_password(client: TestClient, get_test_db, get_test_cache, user_data) -> None:
    setup_user(get_test_db, get_test_cache, user_data)

    wrong_password = "wrongpassword"
    encoded_credentials = base64.b64encode(f"{user_data['email']}:{wrong_password}".encode()).decode()

    data = {"activation_code": user_data["activation_code"]}
    response = client.post("/activate", json=data, headers={"Authorization": f"Basic {encoded_credentials}"})
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication failed. Please check your credentials"

def test_activate_account_already_activated(client: TestClient, get_test_db, get_test_cache, user_data, encoded_credentials) -> None:
    setup_user(get_test_db, get_test_cache, user_data)
    activate_user(user_data["email"], get_test_db)

    data = {"activation_code": user_data["activation_code"]}
    response = client.post("/activate", json=data, headers={"Authorization": f"Basic {encoded_credentials}"})
    
    assert response.status_code == 409
    assert response.json()["detail"] == "This account is already activated"

def test_activate_account_activation_code_expired(client: TestClient, get_test_db, get_test_cache, user_data, encoded_credentials) -> None:
    setup_user(get_test_db, get_test_cache, user_data)
    get_test_cache.delete(user_data["email"])

    data = {"activation_code": user_data["activation_code"]}
    response = client.post("/activate", json=data, headers={"Authorization": f"Basic {encoded_credentials}"})
    
    assert response.status_code == 410
    assert response.json()["detail"] == "The activation code has expired."

def test_activate_account_activation_invalid_code(client: TestClient, get_test_db, get_test_cache, user_data, encoded_credentials) -> None:
    setup_user(get_test_db, get_test_cache, user_data)

    data = {"activation_code": "0000"}
    response = client.post("/activate", json=data, headers={"Authorization": f"Basic {encoded_credentials}"})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "The provided activation code is incorrect"
