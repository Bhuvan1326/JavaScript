"""FastAPI inference endpoint for Evoastra Supply Chain Forecast."""

from fastapi import FastAPI
import joblib
import pandas as pd
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(title="Evoastra Supply Chain Forecast API")

# Get project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model path
model_path = BASE_DIR / "models" / "supply_chain_model.pkl"

# Load trained model
model = joblib.load(model_path)


@app.get("/")
def home():
    """
    Health check endpoint.
    """
    return {"message": "Supply Chain Prediction API running successfully"}


@app.post("/predict")
def predict(data: dict):
    """
    Predict late delivery risk from input features.
    Expected JSON format:
    {
        "Days for shipping (real)": 3,
        "Days for shipment (scheduled)": 2,
        "Benefit per order": 20,
        "Sales per customer": 200
    }
    """

    # Convert incoming JSON to DataFrame
    df = pd.DataFrame([data])

    # Generate prediction
    prediction = model.predict(df)

    return {"prediction": int(prediction[0])}