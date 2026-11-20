from typing import Dict, List
from pydantic import BaseModel, EmailStr, Field, field_validator


class Patient(BaseModel):

  name: str
  email: EmailStr
  age: int
  weight: float
  married: bool
  allergies: List[str]
  contact_details: Dict[str, str]

  # Custom validator to restrict email domains to specific corporate accounts
  @field_validator("email")
  @classmethod # Decorator to make this a class method
  # Syntax: cls refers to the Pydantic model class, and value is the field data being validated
  def email_validator(cls, value):
    valid_domains = ["hdfc.com", "icici.com"]
    # Extract the domain part from the email string (e.g., 'abc@icici.com' -> 'icici.com')
    domain_name = value.split("@")[-1]  # Gets the last part after the '@' symbol (e.g., 'icici.com')

    # Raise an error if the domain is not in the allowed list
    if domain_name not in valid_domains:
      raise ValueError("Not a valid domain")

    return value

  # Custom validator to automatically transform the patient name to uppercase
  @field_validator("name")
  @classmethod
  def transform_name(cls, value):
    return value.upper()

  # Custom validator running in 'after' mode to enforce age boundaries
  @field_validator("age", mode="after")
  @classmethod
  def validate_age(cls, value):
    if 0 < value < 100:
      return value
    else:
      raise ValueError("Age should be in between 0 and 100")


# Function that takes a successfully validated Patient instance and prints details
def update_patient_data(patient: Patient):
  print(patient.name)
  print(patient.age)
  print(patient.allergies)
  print(patient.married)
  print("updated")


# Raw dictionary input data for the patient
patient_info = {
    "name": "nitish",
    "email": "abc@icici.com",
    "age": "30",  # Pydantic type coercion automatically converts string '30' into integer 30
    "weight": 75.2,
    "married": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {"phone": "2353462"},
}

# Instantiate the model, triggering type coercion and all custom field validators
patient1 = Patient(**patient_info)

# Execute the update function using the validated and transformed patient object
update_patient_data(patient1)