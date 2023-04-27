import logging
import os
from time import sleep

import numpy as np
from fastapi import FastAPI, Request, Response
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from joblib import load
from pydantic import BaseModel, Extra
from redis import asyncio

logger = logging.getLogger(__name__)

app = FastAPI()
model = load("model_pipeline.pkl")

LOCAL_REDIS_URL = "redis://localhost:6379/0"


@app.on_event("startup")
def startup():
    HOST_URL = os.environ.get("REDIS_URL", LOCAL_REDIS_URL)
    logger.debug(HOST_URL)
    redis = asyncio.from_url(HOST_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# Use pydantic.Extra.forbid to only except exact field set from client.
# This was not required by the lab.
# Your test should handle the equivalent whenever extra fields are sent.
class House(BaseModel, extra=Extra.forbid):
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


class ListHouses(BaseModel, extra=Extra.forbid):
    houses: list[House]

    def to_np(self):
        return np.vstack([x.to_np() for x in self.houses])


class HousePrediction(BaseModel):
    predictions: list[float]


@app.post("/predict", response_model=HousePrediction)
@cache(expire=60)
async def predict(houses: ListHouses):
    predictions = model.predict(houses.to_np())
    return {"predictions": list(predictions)}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Raises 422 if bad parameter automatically by FastAPI
@app.get("/hello")
async def hello(name: str):
    return {"message": f"Hello {name}"}
