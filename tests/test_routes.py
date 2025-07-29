import json
import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for tests
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Finch API!" in response.data

def test_create_user(client):
    data = {"name": "Shashi", "email": "shashi@example.com"}
    response = client.post('/finch/users', json=data)
    assert response.status_code == 201
    assert response.get_json()["name"] == "Shashi"

def test_get_all_users(client):
    # First create a user
    client.post('/finch/users', json={"name": "Alice", "email": "alice@example.com"})
    response = client.get('/finch/users')
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_get_user_by_id(client):
    # Create a user first
    post_res = client.post('/finch/users', json={"name": "Bob", "email": "bob@example.com"})
    user_id = post_res.get_json()['id']
    # Retrieve user
    response = client.get(f'/finch/users/{user_id}')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Bob'

def test_update_user(client):
    post_res = client.post('/finch/users', json={"name": "Jane", "email": "jane@example.com"})
    user_id = post_res.get_json()['id']
    response = client.put(f'/finch/users/{user_id}', json={"name": "Janet"})
    assert response.status_code == 200
    assert response.get_json()['name'] == "Janet"

def test_delete_user(client):
    post_res = client.post('/finch/users', json={"name": "Mark", "email": "mark@example.com"})
    user_id = post_res.get_json()['id']
    response = client.delete(f'/finch/users/{user_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == "User deleted"

def test_user_not_found(client):
    response = client.get('/finch/users/999')
    assert response.status_code == 404
