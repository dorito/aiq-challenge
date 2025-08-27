from fastapi.testclient import TestClient

from app.main import app
from data.enums import LoginTokenTypeEnum

def test_add_client():
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Cliente teste", "email": "user@example.com", "password": "test"})
        assert response.status_code == 201
        data = response.json()
        assert data['name'] == "Cliente teste"
        assert data['email'] == "user@example.com"
        assert data['created_at'] is not None
        assert data['updated_at'] is not None
        assert data['guid'] is not None

def test_add_repeated_client():
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Cliente teste", "email": "user@example.com", "password": "test"})
        assert response.status_code == 201
        response = client.post("/client/", json={"name": "Cliente teste", "email": "user@example.com", "password": "test"})
        assert response.status_code == 400
        data = response.json()
        assert data['detail'] == "Email already registered"
        
def test_login():
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Cliente teste", "email": "user@example.com", "password": "test"}) # cria usuário

        response = client.post("/client/login", json={"email": "user@example.com", "password": "test"})
        assert response.status_code == 200
        data = response.json()
        assert data['access_token'] is not None
        assert data['token_type'] == LoginTokenTypeEnum.BEARER.value
        assert data['expires_in'] is not None

def test_list_users():
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Cliente teste 1", "email": "user.1@example.com", "password": "test"})
        response = client.post("/client/", json={"name": "Cliente teste 2", "email": "user.2@example.com", "password": "test"})
        response = client.post("/client/", json={"name": "Cliente teste 3", "email": "user.3@example.com", "password": "test"})
        
        response = client.get("/client/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for user in data:
            assert user['name'] in ['Cliente teste 1', 'Cliente teste 2', 'Cliente teste 3']
            assert user['email'] in ['user.1@example.com', 'user.2@example.com', 'user.3@example.com']
            assert 'created_at' in user
            assert 'updated_at' in user
            assert 'guid' in user

def test_edit_user():
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Cliente teste 1", "email": "user.1@example.com", "password": "test"}) # cria usuário
        created_user_data = response.json()
        user_email = created_user_data['email']

        response = client.patch(f"/client/by-email/{user_email}", json={"name": "Cliente teste 1 - Editado", "current_password": "test"})
        assert response.status_code == 200
        edited_data = response.json()
        assert edited_data['name'] == "Cliente teste 1 - Editado"
        assert edited_data['email'] == created_user_data['email']
        assert edited_data['guid'] == created_user_data['guid']
        
def test_edit_user_with_wrong_password():
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Cliente teste 1", "email": "user.1@example.com", "password": "test"}) # cria usuário

        created_user_data = response.json()
        user_email = created_user_data['email']

        response = client.patch(f"/client/by-email/{user_email}", json={"name": "Cliente teste 1 - Editado", "current_password": "wrong password"})
        assert response.status_code == 401
        assert response.json()['detail'] == "Invalid current password"

def test_get_user():
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Cliente teste 1", "email": "user.1@example.com", "password": "test"}) # cria usuário
        created_user_data = response.json()
        user_email = created_user_data['email']

        response = client.get(f"/client/by-email/{user_email}")
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == created_user_data['name']
        assert data['email'] == created_user_data['email']
        assert data['guid'] == created_user_data['guid']

def test_get_user_that_does_not_exist():
    with TestClient(app) as client:
        response = client.get("/client/by-email/fakeuser@example.com")
        assert response.status_code == 404
        assert response.json()['detail'] == "User not found"

def test_delete_user():
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Cliente teste 1", "email": "user.1@example.com", "password": "test"})
        assert response.status_code == 201
        created_user_data = response.json()
        user_email = created_user_data['email']

        response = client.delete(f"/client/by-email/{user_email}")
        assert response.status_code == 204

        response = client.get(f"/client/by-email/{user_email}")
        assert response.status_code == 404
        assert response.json()['detail'] == "User not found"

def test_delete_user_that_does_not_exist():
    with TestClient(app) as client:
        response = client.delete("/client/by-email/nonexistent@example.com")
        assert response.status_code == 404
        assert response.json()['detail'] == "User not found"