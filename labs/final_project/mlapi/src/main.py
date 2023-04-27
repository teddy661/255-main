import logging
import os

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

model_path = "./distilbert-base-uncased-finetuned-sst2"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1,
    return_all_scores=True,
)

logger = logging.getLogger(__name__)
LOCAL_REDIS_URL = "redis://redis:6379"
app = FastAPI()


@app.on_event("startup")
def startup():
    pass


class SentimentRequest(BaseModel):
    pass


class Sentiment(BaseModel):
    pass


class SentimentResponse(BaseModel):
    pass
    # ... [Sentiment]


@app.post("/predict", response_model=SentimentResponse)
def predict(sentiments: SentimentRequest):
    return {"predictions": classifier(sentiments.text)}


@app.get("/health")
async def health():
    return {"status": "healthy"}
