from typing import Dict, List
from pydantic import BaseModel, EmailStr, model_validator


class Patient(BaseModel):

  name: str
  email: EmailStr
  age: int
  weight: float
  married: bool
  allergies: List[str]
  contact_details: Dict[str, str]

  # Syntax: @model_validator(mode='after') validates the entire model instance after individual fields are parsed
  @model_validator(mode="after")
  # Syntax: cls refers to the Pydantic model class, and model is the fully constructed model instance
  def validate_emergency_contact(cls, model):
    # Check if patient is older than 60 and missing an 'emergency' key in their contact details
    if model.age > 60 and "emergency" not in model.contact_details:
      raise ValueError("Patients older than 60 must have an emergency contact")
    return model


# Function that takes a successfully validated Patient instance and prints details
def update_patient_data(patient: Patient):
  print(patient.name)
  print(patient.age)
  print(patient.allergies)
  print(patient.married)
  print("updated")


# Raw dictionary input data for the patient (age is 65, and 'emergency' contact is provided)
patient_info = {
    "name": "nitish",
    "email": "abc@icici.com",
    "age": "65",  # Pydantic type coercion automatically converts string '65' into integer 65
    "weight": 75.2,
    "married": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {"phone": "2353462", "emergency": "235236"},
}

# Instantiate the model, triggering type coercion and the model-level validator
patient1 = Patient(**patient_info)

# Execute the update function using the validated patient object
update_patient_data(patient1)