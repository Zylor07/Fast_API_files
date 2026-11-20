from pydantic import BaseModel

# Define a Pydantic model by inheriting from BaseModel for data validation
class Patient(BaseModel):
    name: str     # Type hint ensuring 'name' is validated as a string
    age: int      # Type hint ensuring 'age' is validated as an integer
    weight: float # Type hint ensuring 'weight' is validated as a float


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
patient_info = {'name': 'pritam', 'age': 23, 'weight': 72} 

# '**' unpacks the dictionary into keyword arguments to instantiate the Patient model
patient1 = Patient(**patient_info) 

insert_patient(patient1)

update_patient(patient1)