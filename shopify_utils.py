import os
import shopify

# Set up Shopify credentials from environment variables
SHOP_URL = os.getenv("ra-labs-interview.myshopify.com")
API_KEY = os.getenv("c23fd1f4ca1554a4d345a40ed0036cee")
PASSWORD = os.getenv("2c0b01510884dc422032349e2f377177")

shopify.ShopifyResource.set_site(f"https://{API_KEY}:{PASSWORD}@{SHOP_URL}/admin")

# Get list of orders
def get_orders():
    orders = shopify.Order.find()
    return [order.to_dict() for order in orders]

# Get specific order by ID
def get_order(order_id):
    order = shopify.Order.find(order_id)
    return order.to_dict()

# Get list of customers
def get_customers():
    customers = shopify.Customer.find()
    return [customer.to_dict() for customer in customers]

# Get specific customer by ID
def get_customer(customer_id):
    customer = shopify.Customer.find(customer_id)
    return customer.to_dict()