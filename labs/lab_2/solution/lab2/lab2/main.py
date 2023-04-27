import numpy as np
from fastapi import FastAPI, HTTPException
from joblib import load
from pydantic import BaseModel, Extra

app = FastAPI()
model = load("model_pipeline.pkl")


# Use pydantic.Extra.forbid to only except exact field set from client.
# This was not required by the lab.
# Your test should handle the equivalent whenever extra fields are sent.
class House(BaseModel, extra=Extra.forbid):
    """Data model to parse the request body JSON."""

    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    def to_np(self):
        return np.array(list(vars(self).values())).reshape(1, 8)


class HousePrediction(BaseModel):
    prediction: float


@app.post("/predict", response_model=HousePrediction)
async def predict(house: House):
    prediction = model.predict(house.to_np())
    return {"prediction": prediction}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Raises 422 if bad parameter automatically by FastAPI
@app.get("/hello")
async def hello(name: str):
    return {"message": f"Hello {name}"}


# /docs endpoint is defined by FastAPI automatically
# /openapi.json returns a json object automatically by FastAPI
