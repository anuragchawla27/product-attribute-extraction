from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.preprocess import clean_text

app = FastAPI(title="Product Attribute Extraction API")

# Load all saved artifacts once at startup
vectorizer = joblib.load("models/vectorizer.pkl")
single_label_models = joblib.load("models/single_label_models.pkl")
multi_label_models = joblib.load("models/multi_label_models.pkl")
multi_label_binarizers = joblib.load("models/multi_label_binarizers.pkl")

SINGLE_LABEL_ATTRS = ["category", "silhouette", "fabric", "neckline", "sleeve", "length"]
MULTI_LABEL_ATTRS = ["embellishment", "color"]


class DescriptionInput(BaseModel):
    description: str


def predict_multilabel(model, X_input, threshold=0.3):
    probas = model.predict_proba(X_input)
    preds = (probas >= threshold).astype(int)
    for i in range(preds.shape[0]):
        if preds[i].sum() == 0:
            top_label_idx = np.argmax(probas[i])
            preds[i, top_label_idx] = 1
    return preds


@app.post("/extract")
def extract_attributes(input_data: DescriptionInput):
    cleaned = clean_text(input_data.description)
    X_input = vectorizer.transform([cleaned])

    result = {}

    for attr in SINGLE_LABEL_ATTRS:
        model = single_label_models[attr]
        pred = model.predict(X_input)[0]
        result[attr.capitalize()] = pred

    for attr in MULTI_LABEL_ATTRS:
        model = multi_label_models[attr]
        mlb = multi_label_binarizers[attr]
        pred_binary = predict_multilabel(model, X_input, threshold=0.3)
        labels = mlb.inverse_transform(pred_binary)[0]
        result[attr.capitalize()] = list(labels)

    return result