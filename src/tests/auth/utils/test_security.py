from src.auth.security import password_matches, get_password_hash  # Adjust the import based on your module structure

# Unit tests for get_password_hash
def test_get_password_hash():
    password = "secure_password"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert password_matches(password, hashed)

def test_get_password_hash_different_salts():
    password = "secure_password"
    hashed1 = get_password_hash(password)
    hashed2 = get_password_hash(password)
    
    # Ensure that hashing the same password results in different hashes due to different salts
    assert hashed1 != hashed2

def test_password_matches_correct_password():
    password = "secure_password"
    hashed = get_password_hash(password)
    
    assert password_matches(password, hashed) is True

def test_password_matches_incorrect_password():
    password = "secure_password"
    incorrect_password = "wrong_password"
    hashed = get_password_hash(password)
    
    assert password_matches(incorrect_password, hashed) is False

def test_password_matches_edge_case_empty_password():
    password = ""
    hashed = get_password_hash(password)
    
    assert password_matches(password, hashed) is True
    assert password_matches("wrong_password", hashed) is False
