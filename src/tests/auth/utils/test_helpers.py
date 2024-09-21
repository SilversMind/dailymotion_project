import pytest
from src.auth.utils import generate_activation_code, validate_email 

def test_generate_activation_code_length():
    code = generate_activation_code(6)
    assert len(code) == 6
    assert code.isdigit()

def test_generate_activation_code_zero_padded():
    code = generate_activation_code(4)
    assert len(code) == 4
    assert code[0] != '0' or code == '0000' 

def test_validate_email_valid():
    valid_email = "test@example.com"
    assert validate_email(valid_email) == valid_email

@pytest.mark.parametrize("invalid_email", [
        ("plainaddress"),
        ("missing@domain"),
        ("user@.com"),
        ("user@domain..com"),
        ("@domain.com"),
    ])
def test_validate_email_invalid_format(invalid_email):
        with pytest.raises(ValueError, match='Invalid email address format'):
            validate_email(invalid_email)

def test_validate_email_valid_with_special_characters():
    valid_email = "user.name+tag+sorting@example.com"
    assert validate_email(valid_email) == valid_email
