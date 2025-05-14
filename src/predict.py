import joblib
import pandas as pd

def make_prediction(model_path, input_data):
    model = joblib.load(model_path)
    prediction = model.predict(input_data)
    return prediction
