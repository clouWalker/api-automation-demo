import pytest
import requests

base_url = "http://localhost:3000"

@pytest.fixture(scope="function", autouse=True)
def reset_data():
    """Reset the data before each test."""
    requests.post(f"{base_url}/reset")

# Test POST /users
def test_post_users_success():
    """Test successful user registration."""
    payload = {"email": "test@example.com", "password": "password123"}
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == payload["email"]

def test_post_users_missing_email():
    """Test user registration with missing email."""
    payload = {"password": "password123"}
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Missing email"

def test_post_users_missing_password():
    """Test user registration with missing password."""
    payload = {"email": "test@example.com"}
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Missing password"

def test_post_users_invalid_email_format():
    """Test user registration with invalid email format."""
    payload = {"email": "invalidemail", "password": "password123"}
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Invalid email format"

def test_post_users_short_password():
    """Test user registration with short password."""
    payload = {"email": "test@example.com", "password": "123"}
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Password too short, minimum 6 characters"

def test_post_users_email_already_registered():
    """Test user registration with an already registered email."""
    payload = {"email": "test@example.com", "password": "password123"}
    # First registration
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 201
    # Second registration with the same email
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 409
    data = response.json()
    assert data["error"] == "Email already registered"

# Test GET /users
def test_get_users_success():
    """Test successful retrieval of user list."""
    # Create some users
    users = [
        {"email": "user1@example.com", "password": "password123"},
        {"email": "user2@example.com", "password": "password123"},
    ]
    for user in users:
        requests.post(f"{base_url}/users", json=user)
    
    # Retrieve users
    response = requests.get(f"{base_url}/users")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "data" in data
    assert len(data["data"]) == len(users)
    for user in data["data"]:
        assert "id" in user
        assert "email" in user

def test_get_users_pagination():
    """Test user list pagination."""
    # Create 15 users
    for i in range(15):
        requests.post(f"{base_url}/users", json={"email": f"user{i}@example.com", "password": "password123"})
    
    # Retrieve first page with default limit
    response = requests.get(f"{base_url}/users", params={"page": 1, "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) == 10

    # Retrieve second page
    response = requests.get(f"{base_url}/users", params={"page": 2, "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["limit"] == 10
    assert len(data["data"]) == 5