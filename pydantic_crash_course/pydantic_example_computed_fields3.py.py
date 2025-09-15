# pydantic Computed Fields 
#for example based on weight and hegiht, we can measure bmi
#for that import computed fields 

from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator , model_validator , computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title="Name of the patient", description="Give the name of the patient", example="Akash")]
    age: int = Field(gt=0, le=120, description="Age of the patient (1-120 years)")  # Adjusted to allow up to 120
    email: EmailStr  # Changed to lowercase for consistency
    linkedin: Optional[AnyUrl] = None  # Optional URL for LinkedIn
    weight: float = Field(gt=0, lt=120, description="Weight in kilograms (0-120)")
    height :float
    married: Optional[bool] = None  # Allow None for optional boolean
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]
    
    @computed_field
    @property
    def bmi_fn(self)->float:
        bmi = round(self.weight/self.height**2,2)
        return bmi

    #work on whole model
    @model_validator(mode='after')
    def validate_emmergency_contact(cls,model):
        if model.age > 60 and 'emmergency' not in model.contact_details:
            raise ValueError("Patient older than 60 must have Emmergency contact")
        return model


    @field_validator('name')
    @classmethod
    def transform_name(cls, value: str) -> str:
        return value.upper()

    @field_validator('email')
    @classmethod
    def email_validator(cls, value: str) -> str:
        valid_domains = ['islamni.com', 'aiub.edu']  # Fixed aiub to aiub.edu
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Invalid domain. Allowed domains: {valid_domains}")
        return value

    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value: int) -> int:
        # Removed redundant check since Field(gt=0, le=120) already enforces this
        return value

def insert_patient_data(patient: Patient) -> None:
    print(f"Name: {patient.name}")
    print(f"Age: {patient.age}")
    print(f"Email: {patient.email}")
    print(f"Weight: {patient.weight}")
    print(f"BMi: {patient.bmi_fn}")
    print("Inserted\n")

# Corrected patient info dictionary
patient_info = {
    'name': 'Mahir',
    'age': 20,
    'email': 'tuser@islamni.com',  # Changed to lowercase key
    'weight': 70.5,
    'height': 7,
    'married': False,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'email': 'tuser@islamni.com',  # Changed to lowercase key
        'phone': '01905293360'
    }
}

# Create patient instance with validation
try:
    patient_1 = Patient(**patient_info)
    insert_patient_data(patient_1)
except ValueError as e:
    print(f"Validation error: {e}")