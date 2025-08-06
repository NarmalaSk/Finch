def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Welcome to the Finch API!" in res.data

def test_get_users(client):
    res = client.get('/finch/users')
    assert res.status_code == 200
    assert b"Test User" in res.data

def test_get_user(client):
    res = client.get('/finch/users/1')
    assert res.status_code == 200
    data = res.get_json()
    assert data['name'] == "Test User"

def test_create_user(client):
    res = client.post('/finch/users', json={
        "name": "New User",
        "email": "new@example.com"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['name'] == "New User"

def test_update_user(client):
    res = client.put('/finch/users/1', json={"name": "Updated User"})
    assert res.status_code == 200
    assert res.get_json()['name'] == "Updated User"

def test_delete_user(client):
    res = client.delete('/finch/users/1')
    assert res.status_code == 200
    assert res.get_json()['message'] == "User deleted"

    # Confirm user is gone
    res2 = client.get('/finch/users/1')
    assert res2.status_code == 404

