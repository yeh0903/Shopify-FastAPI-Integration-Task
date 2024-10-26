from fastapi import FastAPI, HTTPException
from pyactiveresource.connection import ResourceNotFound
import shopify
import os
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

# Load environment variables
load_dotenv()

app = FastAPI()

# Shopify API setup
def setup_shopify():
    shop_url = os.getenv("SHOPIFY_SHOP_URL")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    # check log in info exist
    if not all([shop_url, access_token]):
        raise HTTPException(status_code=500, detail='Shopify credentials not properly configured.')
    
    print(f"Shop URL: {shop_url}")
    session = shopify.Session(shop_url, '2024-01', access_token)
    shopify.ShopifyResource.activate_session(session)
    return shopify

# Rate limiting decorator - 100 points / second
@sleep_and_retry
@limits(calls=100, period=1)
def call_api():
    pass

@app.get("/orders", tags=["Orders"])
def get_orders():
    """
    Retrieve a list of orders from the Shopify store.
    Returns an empty list if no orders exist.
    """
    try:
        call_api()
        setup_shopify()
        orders = shopify.Order.find()
        return [order.to_dict() for order in orders]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders/{order_id}", tags=["Orders"])
def get_order(order_id: int):
    """
    Retrieve details of a specific order by ID. Raise exception if order not found.
    """
    try:
        call_api()
        setup_shopify()
        order = shopify.Order.find(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order.to_dict()
    
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers", tags=["Customers"])
def get_customers():
    """
    Retrieve a list of customers from the Shopify store.
    Returns an empty list if no customers exist.
    """
    try:
        call_api()
        setup_shopify()
        customers = shopify.Customer.find()
        return [customer.to_dict() for customer in customers]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers/{customer_id}", tags=["Customers"])
def get_customer(customer_id: int):
    """
    Retrieve details of a specific customer by ID. Raise exception if customer not found.
    """
    try:
        call_api()
        setup_shopify()
        customer = shopify.Customer.find(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return customer.to_dict()
    
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    try:
        # Check environment variables
        shop_url = os.getenv("SHOPIFY_SHOP_URL")
        access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
        if not all([shop_url, access_token]):
            return {"status": "unhealthy", "detail": "Missing Shopify credentials."}
        
        # Attempt to set up Shopify session
        session = shopify.Session(shop_url, '2024-01', access_token)
        shopify.ShopifyResource.activate_session(session)
        
        # Make a simple API call to check Shopify connection
        shop = shopify.Shop.current()
        return {"status": "healthy"}
    
    except Exception as e:
        # Return unhealthy status with error details
        return {"status": "unhealthy", "detail": str(e)}