from fastapi import FastAPI, HTTPException
import shopify_utils

app = FastAPI()

# Get list of orders from Shopify
@app.get("/orders")
def get_orders():
    try:
        orders = shopify_utils.get_orders()
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get specific order details
@app.get("/orders/{order_id}")
def get_order(order_id: str):
    try:
        order = shopify_utils.get_order(order_id)
        return {"order": order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get list of customers from Shopify
@app.get("/customers")
def get_customers():
    try:
        customers = shopify_utils.get_customers()
        return {"customers": customers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get specific customer details
@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    try:
        customer = shopify_utils.get_customer(customer_id)
        return {"customer": customer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))