import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from pyactiveresource.connection import ResourceNotFound

client = TestClient(app)

# Mock data for orders and customers
mock_order = MagicMock()
mock_order.to_dict.return_value = {
    "id": 000,
    "customer_id": 111,
    "total_price": "100.00",
    "created_at": "2023-10-01T12:00:00Z",
    "status": "paid"
}

mock_customer = MagicMock()
mock_customer.to_dict.return_value = {
    "id": 111,
    "email": "customer@example.com",
    "first_name": "Albert",
    "last_name": "Einstein",
    "orders_count": 10
}

def mock_setup_shopify():
    """
    Mock setup_shopify to do nothing during tests
    """
    pass

@pytest.fixture
def mock_shopify_order_find():
    with patch('shopify.Order.find') as mock_find:
        yield mock_find

@pytest.fixture
def mock_shopify_customer_find():
    with patch('shopify.Customer.find') as mock_find:
        yield mock_find

@pytest.fixture
def mock_call_api():
    with patch('main.call_api') as mock_api:
        yield mock_api

@pytest.fixture
def mock_setup_shopify_fixture():
    with patch('main.setup_shopify', side_effect=mock_setup_shopify) as mock_setup:
        yield mock_setup

def test_health_check(mock_setup_shopify_fixture):
    with patch('shopify.Shop.current') as mock_shop_current:
        mock_shop_current.return_value = MagicMock()
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

def test_get_orders(mock_shopify_order_find):
    mock_shopify_order_find.return_value = [mock_order]
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.json() == [mock_order.to_dict.return_value]

def test_get_order_success(mock_shopify_order_find):
    mock_shopify_order_find.return_value = mock_order
    response = client.get("/orders/000")
    assert response.status_code == 200
    assert response.json() == mock_order.to_dict.return_value

def test_get_order_not_found(mock_shopify_order_find):
    mock_shopify_order_find.side_effect = ResourceNotFound(response=MagicMock(msg='Not Found'))
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}

def test_get_customers(mock_shopify_customer_find):
    mock_shopify_customer_find.return_value = [mock_customer]
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == [mock_customer.to_dict.return_value]

def test_get_customer_success(mock_shopify_customer_find):
    mock_shopify_customer_find.return_value = mock_customer
    response = client.get("/customers/111")
    assert response.status_code == 200
    assert response.json() == mock_customer.to_dict.return_value

def test_get_customer_not_found(mock_shopify_customer_find):
    mock_shopify_customer_find.side_effect = ResourceNotFound(response=MagicMock(msg='Not Found'))
    response = client.get("/customers/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}