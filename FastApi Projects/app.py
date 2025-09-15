from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd
from Schema.prediction_response import PredictionResponse

#import the user input 
from Schema.UserInput import UserInput
from model.predict import predict_output,model,MODEL_VERSION

app = FastAPI()

#Home endpoint

@app.get('/')

def home():
    return {'message':'This is your home '}   

#status or api 
@app.get('/health')

def health_check():
    return{
        'status':'OK',
        'version': MODEL_VERSION,
        'Model_loaded':  model is not None
    }

@app.post('/predict',response_model=PredictionResponse)

def predict_premium(data:UserInput):
    user_input = (
        
            {
                'bmi': data.bmi, 
                'age_group' : data.age_group,
                'lifestyle_risk': data.lifestyle_risk,
                'city_tier' : data.city_tier,
                'income_lpa' : data.income_lpa,
                'occupation' : data.occupation
            }
    )
    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'Response':prediction})
    except Exception as e : 
        return JSONResponse(status_code=500,content=str(e))
