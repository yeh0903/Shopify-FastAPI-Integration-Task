from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

# Test endpoint for fetching orders
@patch("shopify_utils.get_orders")
def test_get_orders(mock_get_orders):
    mock_get_orders.return_value = [{"id": 1, "name": "Test Order"}]
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.json() == {"orders": [{"id": 1, "name": "Test Order"}]}

# Test endpoint for fetching specific order
@patch("shopify_utils.get_order")
def test_get_order(mock_get_order):
    mock_get_order.return_value = {"id": 1, "name": "Test Order"}
    response = client.get("/orders/1")
    assert response.status_code == 200
    assert response.json() == {"order": {"id": 1, "name": "Test Order"}}

# Test endpoint for fetching customers
@patch("shopify_utils.get_customers")
def test_get_customers(mock_get_customers):
    mock_get_customers.return_value = [{"id": 1, "name": "Test Customer"}]
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == {"customers": [{"id": 1, "name": "Test Customer"}]}

# Test endpoint for fetching specific customer
@patch("shopify_utils.get_customer")
def test_get_customer(mock_get_customer):
    mock_get_customer.return_value = {"id": 1, "name": "Test Customer"}
    response = client.get("/customers/1")
    assert response.status_code == 200
    assert response.json() == {"customer": {"id": 1, "name": "Test Customer"}}