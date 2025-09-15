# export pydantic model as python dictionary or json 

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


#export as a dictionary 
save_as_dictionary = patient1.model_dump()
print(save_as_dictionary)
print(type(save_as_dictionary))

#Export as a Json 
save_as_json = patient1.model_dump_json()
print(save_as_json)
print(type(save_as_json))


#control parameters
#include
#export as a dictionary 
save_as_dictionary = patient1.model_dump(include=['name'])
print(save_as_dictionary)
print(type(save_as_dictionary))

#Exclude 

save_as_dictionary = patient1.model_dump(exclude=['name'])
print(save_as_dictionary)
print(type(save_as_dictionary))


#Exclude set 

#don't set what wasn't set during the object crating proces 