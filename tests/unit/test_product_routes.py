from fastapi.testclient import TestClient
from ..mock_product_service import MockProductService
from product.routes import product_service
from fastapi import Request
from app.main import app

async def override_product_service(request: Request):
    return MockProductService()

def test_list_products():
    app.state.testing = True
    app.dependency_overrides[product_service] = override_product_service
    with TestClient(app) as client:
        response = client.get("/product/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5
        for item in data:
            assert "id" in item
            assert "title" in item
            assert "price" in item
            assert "description" in item
            assert "category" in item
            assert "image" in item
            assert "rating" in item
            
def test_get_product_by_id():
    app.state.testing = True
    app.dependency_overrides[product_service] = override_product_service
    with TestClient(app) as client:
        response = client.get("/product/by-id/1")
        assert response.status_code == 200
        data = response.json()
        assert not isinstance(data, list)
        assert "id" in data
        assert "title" in data
        assert "price" in data
        assert "description" in data
        assert "category" in data
        assert "image" in data
        assert "rating" in data