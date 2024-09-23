from fastapi.testclient import TestClient
from src.auth.database import save_user, UserRegistration, activate_user

def test_register_user_success(client: TestClient) -> None:
    data = {"email": "johndoe@example.com", "password": "azertyuiop"}
    response = client.post("/register", json=data)
    
    assert response.status_code == 201
    assert response.json()["message"] == (
        "User registered sucessfully. Please check your email for the activation code"
    )

def test_register_user_already_exists_unactivated(client: TestClient, get_test_db) -> None:
    save_user(UserRegistration(email="johndoe@example.com", password="azertyuiop"), get_test_db)
    
    data = {"email": "johndoe@example.com", "password": "azertyuiop"}
    response = client.post("/register", json=data)

    assert response.status_code == 201
    assert response.json()["message"] == "Activation code is still valid. Please check your email."

def test_register_user_already_exists_activated(client: TestClient, get_test_db) -> None:
    save_user(UserRegistration(email="johndoe@example.com", password="azertyuiop"), get_test_db)
    
    data = {"email": "johndoe@example.com", "password": "azertyuiop"}
    response = client.post("/register", json=data)
    activate_user(data["email"], get_test_db)
    response = client.post("/register", json=data)

    assert response.status_code == 409
    assert response.json()["detail"] == "This email is already taken"
    
    activate_user(data["email"], get_test_db)
    response = client.post("/register", json=data)

    assert response.status_code == 409
    assert response.json()["detail"] == "This email is already taken"


def test_register_user_activation_code_cached(client: TestClient, get_test_cache) -> None:
    data = {"email": "alice@example.com", "password": "password456"}
    client.post("/register", json=data)

    cached_code = get_test_cache.get("alice@example.com")
    assert cached_code is not None 

def test_register_user_invalid_data(client: TestClient) -> None:
    data = {"email": "bobexample.com", "password": "dsq"}
    response = client.post("/register", json=data)

    assert response.status_code == 400


