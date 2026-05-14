"""
Churn Prediction API

Run with:
    litestar --app main:app run --reload
Then open:
    http://localhost:8000/schema/swagger
"""

import pandas as pd
from litestar import Litestar,get,post
from pydantic import BaseModel, ConfigDict
from app.model_utils import predict_churn
from app.model_utils import encoder

from app.logger_setup import setup_logging

logger = setup_logging()


# ---------------------------------------------------------------------------
# Request Schema
# ---------------------------------------------------------------------------
class ChurnRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    CreditScore: float
    Geography: str
    Gender: str
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: int
    EstimatedSalary: int



# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

# TODO 2: Create a GET endpoint at "/" that returns a welcome message
#         Log that the home endpoint was accessed
@get("/")
async def home() -> dict[str, str]:
    logger.info("Home endpoint accessed")
    return {"message": "Welcome to the Churn Prediction API!"}

# TODO 3: Create a GET endpoint at "/health" that returns {"status": "healthy"}
@get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}

# TODO 4: Create a POST endpoint at "/predict" that:
#         - Accepts a ChurnRequest as the data parameter
#         - Extracts features into a list
#         - Calls predict_churn(features)
#         - Returns the prediction
#         - Logs the input features and the prediction result
@post("/predict")
async def predict(data: ChurnRequest) -> dict[str, int]:
    features= [
        data.CreditScore,
        data.Geography,
        data.Gender,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.HasCrCard,
        data.IsActiveMember,
        data.EstimatedSalary,
    ]

    columns = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
    features_df = pd.DataFrame([features], columns=columns)
    transformed_features = encoder.transform(features_df) 
    
    # model.predict expects a 2D array, which transformed_features is
    prediction = int(predict_churn(transformed_features.tolist()))
    
    logger.info(f"Prediction made for input: {features} - Result: {prediction}")
    return {"prediction": prediction}
# ---------------------------------------------------------------------------
# App

# ---------------------------------------------------------------------------
# TODO 5: Register your endpoint functions in the list below
app = Litestar(
    route_handlers=[home, health, predict],
)
