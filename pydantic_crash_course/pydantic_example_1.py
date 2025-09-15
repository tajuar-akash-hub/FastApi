#anyurl = to validate url , emailstr: to validate email ,  field = to add logic, like greater than or less than
#optinal = as the name suggest 
#field = also to add metadata - to let people know what is the purpose 
#annotated = to use metadata

#field validator : works in two nodes, 1) before nodes 2) after nodes  , by default it is after, after measn 

from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    
    name: Annotated[str, Field(max_length=50, title="Name of the patient", description="Give the name of the patient", example="Akash")]
    age: int = Field(gt=0, le=120, description="Age of the patient (1-120 years)")  # Adjusted to allow up to 120
    email: EmailStr  # Changed to lowercase for consistency
    linkedin: Optional[AnyUrl] = None  # Optional URL for LinkedIn
    weight: float = Field(gt=0, lt=120, description="Weight in kilograms (0-120)")
    married: Optional[bool] = None  # Allow None for optional boolean
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

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
    print("Inserted\n")

# Corrected patient info dictionary
patient_info = {
    'name': 'Mahir',
    'age': 22,
    'email': 'tuser@islamni.com',  # Changed to lowercase key
    'weight': 70.5,
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