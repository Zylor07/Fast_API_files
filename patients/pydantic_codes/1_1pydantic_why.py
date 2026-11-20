from pydantic import BaseModel
from typing import List,Dict




# Define a Pydantic model by inheriting from BaseModel for data validation
class Patient(BaseModel):
    name: str     # Type hint ensuring 'name' is validated as a string
    age: int      # Type hint ensuring 'age' is validated as an integer
    weight: float # Type hint ensuring 'weight' is validated as a float
    married:bool
    allergies:List[str] #it is a list {which value is str}
    contact_details:Dict[str,str] #key is string and value is string {its a key value pair}


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
patient_info = {'name': 'pritam', 'age': 23, 'weight': 72,'married':True,'allergies':['pollen','dust'],'contact_details':{'email':'pritam2055626@gmail.com','phone_no':'7478396102'}} 

# '**' unpacks the dictionary into keyword arguments to instantiate the Patient model
patient1 = Patient(**patient_info) 

insert_patient(patient1)

update_patient(patient1)