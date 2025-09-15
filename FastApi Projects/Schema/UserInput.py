from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd

#import from the config 
from config.city_tier import tier_1_cities, tier_2_cities

#pydantic model to validate incoming data 
class UserInput(BaseModel):
    age: Annotated[int,Field(...,gt=0,lt=120,description="Age of the user")]
    weight:Annotated[float,Field(...,gt=0,lt=120.5,description="weight of the user")]
    height: Annotated[float,Field(...,gt=0,lt=2.5,description="Age of the user")]
    income_lpa : Annotated[float,Field(...,gt=0,description="Income of the user")]
    smoker : Annotated[bool,Field(...,description="Smoker verdict of the user")]
    city:Annotated[str,Field(...,description="city of the user")]
    occupation:Annotated[Literal['retired','freelancer','student'],Field(...,description="Age of the user")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/self.height**2
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi >30:
            return "high"
        elif self.smoker or self.bmi >27:
            return "medium"
        else :
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "Senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
         if self.city in tier_1_cities:
            return 1
         elif self.city in tier_2_cities:
            return 2
         else:
             return 3
         
    # title case means first letter is capital
    @field_validator("city")
    def normalize_city(cls, v: str) -> str:
        return v.strip().title()