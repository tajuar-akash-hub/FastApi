#nested model means ; if you want to use one in another model as a field, then we use nested model
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}
address1 = Address(**address_dict)

patient_dict = {'name': 'Mahir', 'gender': 'male', 'age': 10, 'address': address1}
patient1 = Patient(**patient_dict)
print(patient1.address)