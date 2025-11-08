import pickle

from fastapi import FastAPI

from digits_recognition.server.config import MODEL_PATH
from digits_recognition.types.server_types import Item

model = pickle.load(open(MODEL_PATH, "rb"))


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict/")
def predict_digit(item: Item):
    prediction = model.predict([item.image_data])
    return {"prediction": int(prediction[0])}
