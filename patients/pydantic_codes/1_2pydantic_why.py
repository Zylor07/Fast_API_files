from pydantic import BaseModel
from typing import List,Dict,Optional




# Define a Pydantic model by inheriting from BaseModel for data validation
class Patient(BaseModel):
    name: str     # Type hint ensuring 'name' is validated as a string   |
    age: int      # Type hint ensuring 'age' is validated as an integer  |
    weight: float # Type hint ensuring 'weight' is validated as a float  | ------>These all are required field 
    married:bool =False # set the default value as false                 --->OPtional field
    allergies:Optional[List[str]] = None #it is a list {which value is str} and we make it optional field and set the default value as None --->OPtional field
    contact_details:Dict[str,str] #key is string and value is string {its a key value pair} ------>These all are required field 


def insert_patient(patient_obj: Patient): 
    # Accepts a Patient object and prints its attributes
    print(patient_obj.name) 
    print(patient_obj.age) 


def update_patient(patient_obj: Patient): 
    # Accepts a Patient object and prints all three attributes
    print(patient_obj.name) 
    print(patient_obj.age) 
    print(patient_obj.weight) 


# Storing raw patient information in a dictionary
#see there is no allergy field required 
patient_info = {'name': 'pritam', 'age': 23, 'weight': 72,'married':True,'contact_details':{'email':'pritam2055626@gmail.com','phone_no':'7478396102'}} 

# '**' unpacks the dictionary into keyword arguments to instantiate the Patient model
patient1 = Patient(**patient_info) 

insert_patient(patient1)

update_patient(patient1)