from fastapi import FastAPI , HTTPException , Query , Path
import json
from pydantic import BaseModel, Field  ,computed_field
from typing import Annotated , Literal,Optional
from fastapi.responses import JSONResponse

app = FastAPI()

# to create 
class patient(BaseModel):
    id: Annotated[str, Field(..., description="Patient id field", examples=['P001'])]
    name: Annotated[str, Field(..., description='name of the patient')]
    city: Annotated[str, Field(..., description='City name')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Patient Age')]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="Patient Gender")]
    height: Annotated[int, Field(..., gt=0, description='Height of the patient')]
    weight: Annotated[int, Field(..., gt=0, description='Weight of the patient')]

    @computed_field
    @property
    def bmi(self) -> float:
        # Convert height from cm to m if needed
        bmi = round(self.weight / (self.height / 100) ** 2, 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'


# to update patient 

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# to load data 
def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

#to save data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {'message' : "Patient Management System Api " }

@app.get('/about')
def about():
    return {
        'message' :
        "A fully functinal Patient Managemnt System "
    }

@app.get('/status')
def status():
    return {
        'Status' : "API Is running"
    }

@app.get('/view')
def view():
    data = load_data()
    return data

#filter by patient id 

@app.get('/patient/{patient_id}')
def view_patient_details(patient_id : str = Path(..., description="ID of the patient from the DB" , example='P001')):

    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404 ,detail='Patinet not found')


# add a query to sort 

@app.get('/sort')

def sort_patient( sort_by :str = Query(..., description= "Sort on the basis of height, wright or bmi" ), order:str = Query('asc',description="sort in asc or desc order")):

    valud_fields = ['height','weight','bmi']

    if sort_by not in valud_fields:
        raise HTTPException(status_code = 400 , detail='Invalid field select from {valud_fields}') #404 error from client side
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid order, avaialbe asc/desc")
    
    data = load_data()
    sort_order = True if order =='desc' else False

    sorted_data = sorted( data.values() , key = lambda x:x.get(sort_by,0), reverse=sort_order )
    return sorted_data
    

# Create patient 

@app.post('/create')

def create_patient(patient:patient):
    # We'd follow there steps 

    # 1) load existing data 
    data = load_data()

    # 2) check if the patient already exist 
    if patient.id in data:
        raise HTTPException(status_code=400, detail="patient alreaydy exist")
    
    # 3) new patient add to the database  , json to dictionary conversion 
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # 4) Save file into the json file 
    save_data(data)

    #5) tell client about the wrok success
    return JSONResponse(status_code=201,content={'message':'patient created done'})

# to update 
@app.put('/edit/{patient_id}')

def patient_update(patient_id : str,patient_update : PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient Not found')
    
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True) # exclude to avoid not updated value

    # run a loop to update 
    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value

    #problamatic part  : bmi and verdit need to calculate again 
    #steps : existing patient info -> pydantic object -> updated bmi + verdict 

    existing_patient_info['id'] = patient_id  #there is no id in the previus , so we added it
    patient_pydantic_obj = patient(**existing_patient_info)

    #python object to dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    #add this dict to data
    data[patient_id] = existing_patient_info

    #save data 
    save_data(data)

    #show confimatin 

    return JSONResponse(status_code=200, content={'message': 'successfully  updated'})



# to delete 



@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    del data[patient_id]
    save_data(data)  # Save the updated data

    return JSONResponse(status_code=200, content={'message': 'deleted successfully'})
    