# Shopify-FastAPI-Integration-Task

## Features
- Retrieve Orders: Fetch a list of orders or a specific order by ID.
- Retrieve Customers: Fetch a list of customers or a specific customer by ID.
- Health Check Endpoint: Verify the API is running and connected to Shopify.
- Rate Limiting: Implement rate limiting to comply with Shopify API usage limits.

## Prerequisites
- Python 3.7+ and packages listed in requirements.txt
- Shopify Store: Access to a Shopify store and API credentials.

## Setup
1. Clone the repository.
2. Install requirements: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file.

## Running the Project
- Run the FastAPI service: `uvicorn main:app --reload`

## API Endpoints and Server
- Access the API documentation at 'http://localhost:8000/docs'
- `GET /orders`: Retrieve all orders
- `GET /orders/{order_id}`: Retrieve specific order (order ID)
- `GET /customers`: Retrieve all customers
- `GET /customers/{customer_id}`: Retrieve specific customer (customer ID)

## Security Consideration
- Always use environment variables for sensitive credentials
- Never commit the .env file to version control