from fastapi import FastAPI
from pydantic import BaseModel, Field,computed_field
from typing import Literal,Annotated
from fastapi.responses import JSONResponse
import joblib
import pandas as pd

def load_model():
    try:
        return joblib.load('model.pkl'), None
    except Exception as exc:
        return None, str(exc)

# Load model safely so app import does not crash deployment health checks.
model, model_load_error = load_model()


app = FastAPI()

tier_1_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai",
    "Kolkata", "Hyderabad", "Pune"
]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi",
    "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara",
    "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati",
    "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad",
    "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem",
    "Vijayawada", "Tiruchirappalli", "Bhavnagar", "Gwalior",
    "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode",
    "Warangal", "Kolhapur", "Bilaspur", "Jalandhar", "Noida",
    "Guntur", "Asansol", "Siliguri"
]


# Pydantic model for input validation
class InputData(BaseModel):
    age: Annotated[int, Field(..., gt = 0, lt =100, description="Age must be between 1 and 99")]
    weight: Annotated[float, Field(..., gt = 0, description="weight of user")]
    height: Annotated[float, Field(..., gt = 0,lt =2.5, description="height of user")]
    income_lpa: Annotated[float, Field(..., gt = 0, description="Salary of user")]
    smoker: Annotated[bool, Field(..., description="Is the user a smoker?")]
    city: Annotated[str, Field(..., description="City of residence")]
    occupation: Annotated[Literal["retired", "freelancer", "student", "government_job", "business_owner", "unemployed", "private_job"], Field(..., description="Occupation of the user")]

# and also computes new fields required for prediction
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif 25 <= self.age < 45:
            return "adult"
        elif 45 <= self.age < 65:
            return "middle_aged"
        else:
            return "senior"
    @computed_field 
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post("/predict")
def predict_premium(data: InputData):
    if model is None:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Model failed to load",
                "details": model_load_error,
            },
        )

    input_df = pd.DataFrame([{
        'bmi' : data.bmi,
        'age_group' : data.age_group,
        'lifestyle_risk' : data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
    }])

    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={"predicted_premium": prediction})