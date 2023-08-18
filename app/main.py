from fastapi import FastAPI, Request
import pickle
import requests
from fastapi.middleware.cors import CORSMiddleware
from app.code import predict_carsbrand

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# model = pickle.load(open(r"../model/carsbrandModel.pkl", "rb"))

model = pickle.load(open(f"model/carsbrandmodel.pkl", "rb"))

endpoint = "http://172.17.0.1:80/api/gethog"


@app.get("/")
def root():
    return {"message": "This is my api"}


@app.post("/api/carbrand")
async def read_str(data: Request):
    item = await data.json()
    hog = requests.get(endpoint, json=item)
    brand = predict_carsbrand(model, hog.json()["hog"])
    return brand
