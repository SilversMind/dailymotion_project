from src.auth.schemas import UserRegistration
from src.auth.database import get_user_by_email, save_user, user_exists, cache_activation_code, activate_user

def test_save_user(get_test_db):
    user = UserRegistration(email="johndoe@example.com", password="securepassword")
    save_user(user, get_test_db)

    # Verify user was saved
    retrieved_user = get_user_by_email(user.email, get_test_db)
    assert retrieved_user is not None
    assert retrieved_user.email == user.email

def test_get_user_by_email(get_test_db):
    email = "existing_user@example.com"
    user = UserRegistration(email=email, password="securepassword")
    save_user(user, get_test_db)

    retrieved_user = get_user_by_email(email, get_test_db)
    assert retrieved_user is not None
    assert retrieved_user.email == email

def test_activate_user(get_test_db):
    email = "activate_user@example.com"
    user = UserRegistration(email=email, password="securepassword")
    save_user(user, get_test_db)

    activate_user(email, get_test_db)
    activated_user = get_user_by_email(email, get_test_db)

    assert activated_user.activation_status

def test_user_exists(get_test_db):
    email = "check_user@example.com"
    user = UserRegistration(email=email, password="securepassword")
    save_user(user, get_test_db)

    assert user_exists(email, get_test_db) is True
    assert user_exists("nonexistent@example.com", get_test_db) is False

def test_cache_activation_code(get_test_cache):
    email = "cache_user@example.com"
    activation_code = "1234"

    cache_activation_code(email, activation_code, get_test_cache)
    cached_code = get_test_cache.get(email)

    assert cached_code.decode() == activation_code
