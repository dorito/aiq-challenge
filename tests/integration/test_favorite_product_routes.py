from fastapi.testclient import TestClient
from ..mock_product_service import MockProductService
from favorite_product.service import FavoriteProductService
from favorite_product.routes import favorite_product_service
from fastapi import Request
from app.main import app

async def override_favorite_product_service(request: Request):
    return FavoriteProductService(cache=request.app.cache, product_service=MockProductService())
  
def test_add_favorite_product_unauthorized():
    app.dependency_overrides[favorite_product_service] = override_favorite_product_service
    with TestClient(app) as client:
        response = client.post("/favorite-product/", json={"product_id": 1})
        assert response.status_code == 401
        assert response.json()['detail'] == "Unauthorized"

def test_add_favorite_product():
    app.dependency_overrides[favorite_product_service] = override_favorite_product_service
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Usuário", "email": "user@example.com", "password": "password"}) # cria usuário
        response = client.post("/client/login", json={"email": "user@example.com", "password": "password"}) # loga no usuário
        login_data = response.json()

        response = client.post("/favorite-product/", json={"product_id": 1}, headers={"Authorization": f"Bearer {login_data['access_token']}"})
        assert response.status_code == 201
        data = response.json()
        assert data['id'] == 1
        assert data['title'] is not None
        assert data['price'] is not None
        assert data['description'] is not None
        assert data['category'] is not None
        assert data['image'] is not None
        assert 'rating' in data

def test_add_favorite_product_should_fail_a_second_time():
    app.dependency_overrides[favorite_product_service] = override_favorite_product_service
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Usuário", "email": "user@example.com", "password": "password"}) # cria usuário
        response = client.post("/client/login", json={"email": "user@example.com", "password": "password"}) # loga no usuário
        login_data = response.json()

        response = client.post("/favorite-product/", json={"product_id": 1}, headers={"Authorization": f"Bearer {login_data['access_token']}"}) # cria o vínculo entre usuário e produto
        assert response.status_code == 201
        data = response.json()
        assert data['id'] == 1
        assert data['title'] is not None
        assert data['price'] is not None
        assert data['description'] is not None
        assert data['category'] is not None
        assert data['image'] is not None
        assert 'rating' in data
        
        response = client.post("/favorite-product/", json={"product_id": 1}, headers={"Authorization": f"Bearer {login_data['access_token']}"}) # cria o vínculo entre usuário e produto
        assert response.status_code == 400
        assert response.json()['detail'] == "Favorite product already exists"

def test_list_favorite_products_unauthorized():
    with TestClient(app) as client:
        response = client.get("/favorite-product/")
        assert response.status_code == 401
        assert response.json()['detail'] == "Unauthorized"

def test_list_favorite_products():
    app.dependency_overrides[favorite_product_service] = override_favorite_product_service
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Usuário", "email": "user@example.com", "password": "password"}) # cria usuário
        response = client.post("/client/login", json={"email": "user@example.com", "password": "password"}) # loga no usuário
        login_data = response.json()
        
        response = client.post("/favorite-product/", json={"product_id": 1}, headers={"Authorization": f"Bearer {login_data['access_token']}"}) # cria o vínculo entre usuário e produto
        response = client.post("/favorite-product/", json={"product_id": 2}, headers={"Authorization": f"Bearer {login_data['access_token']}"}) # cria o vínculo entre usuário e produto
        response = client.post("/favorite-product/", json={"product_id": 3}, headers={"Authorization": f"Bearer {login_data['access_token']}"}) # cria o vínculo entre usuário e produto
        
        response = client.get("/favorite-product/", headers={"Authorization": f"Bearer {login_data['access_token']}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        
        for item in data:
            assert item['id'] is not None
            assert item['title'] is not None
            assert item['price'] is not None
            assert item['description'] is not None
            assert item['category'] is not None
            assert item['image'] is not None
            assert 'rating' in item

def test_list_favorite_products_cannot_see_list_from_another_user():
    app.dependency_overrides[favorite_product_service] = override_favorite_product_service
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Usuário", "email": "user.1@example.com", "password": "password"}) # cria usuário
        response = client.post("/client/login", json={"email": "user.1@example.com", "password": "password"}) # loga no usuário
        first_login_data = response.json()
        response = client.post("/client/", json={"name": "Usuário", "email": "user.2@example.com", "password": "password"}) # cria usuário
        response = client.post("/client/login", json={"email": "user.2@example.com", "password": "password"}) # loga no usuário
        second_login_data = response.json()

        response = client.post("/favorite-product/", json={"product_id": 1}, headers={"Authorization": f"Bearer {first_login_data['access_token']}"}) # cria o vínculo entre usuário e produto
        response = client.post("/favorite-product/", json={"product_id": 2}, headers={"Authorization": f"Bearer {first_login_data['access_token']}"}) # cria o vínculo entre usuário e produto
        response = client.post("/favorite-product/", json={"product_id": 3}, headers={"Authorization": f"Bearer {second_login_data['access_token']}"}) # cria o vínculo entre usuário e produto

        response = client.get("/favorite-product/", headers={"Authorization": f"Bearer {first_login_data['access_token']}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        
        response = client.get("/favorite-product/", headers={"Authorization": f"Bearer {second_login_data['access_token']}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

def test_delete_favorite_product_unauthorized():
    app.dependency_overrides[favorite_product_service] = override_favorite_product_service
    with TestClient(app) as client:
        response = client.delete("/favorite-product/by-product-id/1")
        assert response.status_code == 401
        assert response.json()['detail'] == "Unauthorized"

def test_delete_favorite_product():
    app.dependency_overrides[favorite_product_service] = override_favorite_product_service
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Usuário", "email": "user@example.com", "password": "password"}) # cria usuário
        response = client.post("/client/login", json={"email": "user@example.com", "password": "password"}) # loga no usuário
        login_data = response.json()

        response = client.post("/favorite-product/", json={"product_id": 1}, headers={"Authorization": f"Bearer {login_data['access_token']}"}) # cria o vínculo entre usuário e produto

        response = client.delete("/favorite-product/by-product-id/1", headers={"Authorization": f"Bearer {login_data['access_token']}"})
        assert response.status_code == 204

        response = client.get("/favorite-product/", headers={"Authorization": f"Bearer {login_data['access_token']}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

def test_delete_favorite_product_that_isnt_favorited():
    app.dependency_overrides[favorite_product_service] = override_favorite_product_service
    with TestClient(app) as client:
        response = client.post("/client/", json={"name": "Usuário", "email": "user@example.com", "password": "password"}) # cria usuário
        response = client.post("/client/login", json={"email": "user@example.com", "password": "password"}) # loga no usuário
        login_data = response.json()

        response = client.delete("/favorite-product/by-product-id/999", headers={"Authorization": f"Bearer {login_data['access_token']}"})
        assert response.status_code == 404
        assert response.json()['detail'] == "Favorite product not found"
