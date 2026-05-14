"""
Tests for the Churn Prediction API.

Run with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
"""
import pandas as pd
from litestar.testing import TestClient
from app.model_utils import predict_churn, encoder
from main import app

# ---------------------------------------------------------------------------
# Function Tests
# ---------------------------------------------------------------------------

# TODO 1: Write a test that calls predict_churn() directly with sample features
#         and asserts the result is 0 or 1
#         Hint: import predict_churn from app.model_utils
def test_predict_churn_function():
    sample_data = [[600, 'France', 'Male', 42, 2, 0, 1, 1, 1, 101348]]
    columns = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
    sample_df = pd.DataFrame(sample_data, columns=columns)
    transformed_features = encoder.transform(sample_df).tolist()
    
    result = predict_churn(transformed_features)
    assert result in [0, 1]

# TODO 2 (bonus): Write another function test with edge-case inputs
def test_predict_churn_edge_cases():
    # Testing with extreme/unusual values (e.g. 0 CreditScore, 105 Age, negative Balance)
    sample_data = [[0, 'Germany', 'Female', 105, 10, -50000, 10, 0, 0, 0]]
    columns = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
    sample_df = pd.DataFrame(sample_data, columns=columns)
    transformed_features = encoder.transform(sample_df).tolist()
    
    result = predict_churn(transformed_features)
    assert result in [0, 1]

# ---------------------------------------------------------------------------
# Endpoint Tests
# ---------------------------------------------------------------------------

# TODO 3: Write a test that POSTs to /predict with valid JSON
#         and checks the status code and response body
#         Hint: Litestar POST returns 201, not 200
#         Hint: use `with TestClient(app=app) as client:`
def test_predict_endpoint():
    with TestClient(app=app) as client:
        payload = {
            "CreditScore": 600,
            "Geography": "France",
            "Gender": "Male",
            "Age": 42,
            "Tenure": 2,
            "Balance": 0,
            "NumOfProducts": 1,
            "HasCrCard": 1,
            "IsActiveMember": 1,
            "EstimatedSalary": 101348
        }
        res = client.post("/predict", json=payload)
        assert res.status_code == 201
        data = res.json()
        assert "prediction" in data
        assert data["prediction"] in [0, 1]

# TODO 4: Write a test for GET /health
def test_health_endpoint():
    with TestClient(app=app) as client:
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json() == {"status": "healthy"}

# TODO 5: Write a test for GET /
def test_home_endpoint():
    with TestClient(app=app) as client:
        res = client.get("/")
        assert res.status_code == 200
        assert res.json() == {"message": "Welcome to the Churn Prediction API!"}

# TODO 6 (bonus): Test that invalid input returns status 400
def test_predict_endpoint_invalid_input():
    with TestClient(app=app) as client:
        # Pass an extra feature ("Exited") to trigger the "forbid" validation rule
        payload = {
            "CreditScore": 600,
            "Geography": "France",
            "Gender": "Male",
            "Age": 42,
            "Tenure": 2,
            "Balance": 0,
            "NumOfProducts": 1,
            "HasCrCard": 1,
            "IsActiveMember": 1,
            "EstimatedSalary": 101348,
            "Exited": 0  # This should trigger a 400 Bad Request
        }
        res = client.post("/predict", json=payload)
        assert res.status_code == 400
