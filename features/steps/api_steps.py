"""
Step definitions for the API feature files.
"""

from behave import given, when, then
import json
from utils.api_client import APIClient
from utils.pydantic_models import Product
from utils.ai_data_generator import generate_product_payload

# Global client – in real code you may use context instead
api_client: APIClient = None
latest_response: dict = {}

@given('the API client is initialized')
def step_init_client(context):
    global api_client
    api_client = APIClient(
        base_url="https://fakestoreapi.com",
        token_url="/auth/login",
        username="admin",
        password="admin123"
    )

@when('I request a token with username "{username}" and password "{password}"')
def step_request_token(context, username, password):
    global latest_response
    latest_response = api_client.post("/auth/login", json={"username": username, "password": password})

@then('the response contains a field "{field}"')
def step_check_field(context, field):
    assert field in latest_response, f"Missing field {field}"

@given('the payload for a new product is generated')
def step_generate_payload(context):
    context.payload = generate_product_payload()

@when('I POST to "/products" with the payload')
def step_post_product(context):
    global latest_response
    latest_response = api_client.post("/products", json=context.payload)

@then('the response matches the "Product" schema')
def step_validate_schema(context):
    product = Product(**latest_response)  # will raise if validation fails
    assert isinstance(product, Product)