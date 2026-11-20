from typing import Dict, List
from pydantic import BaseModel, EmailStr, computed_field


class Patient(BaseModel):

  name: str
  email: EmailStr
  age: int
  weight: float  # kg
  height: float  # mtr
  married: bool
  allergies: List[str]
  contact_details: Dict[str, str]

  # Syntax: @computed_field allows you to include a custom calculated property when exporting/serializing the model
  @computed_field
  # Syntax: @property allows this method to be accessed like a normal attribute (e.g., patient.bmi instead of patient.bmi())
  @property
  def bmi(self) -> float:
    # Calculate Body Mass Index: weight (kg) divided by height squared (m^2), rounded to 2 decimal places
    bmi = round(self.weight / (self.height**2), 2)
    return bmi


# Function that takes a successfully validated Patient instance and prints details
def update_patient_data(patient: Patient):
  print(patient.name)
  print(patient.age)
  print(patient.allergies)
  print(patient.married)
  print("BMI", patient.bmi)  # Accessing the computed field like a standard attribute
  print("updated")


# Raw dictionary input data for the patient (added 'height': 1.72 to support the BMI calculation)
patient_info = {
    "name": "nitish",
    "email": "abc@icici.com",
    "age": "65",  # Pydantic type coercion automatically converts string '65' into integer 65
    "weight": 75.2,
    "height": 1.72,
    "married": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {"phone": "2353462", "emergency": "235236"},
}

# Instantiate the model, triggering type coercion and calculating the computed fields
patient1 = Patient(**patient_info)

# Execute the update function using the validated patient object
update_patient_data(patient1)