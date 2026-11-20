from typing import Annotated, Dict, List, Optional
from pydantic import AnyUrl, BaseModel, EmailStr, Field


# Define a Pydantic model to validate patient data
class Patient(BaseModel):

  # Field with max length validation, title, description, and examples
  name: Annotated[
      str,
      Field(
          max_length=50,
          title="Name of the patient",
          description="Give the name of the patient in less than 50 chars",
          examples=["Nitish", "Amit"],
      ),
  ]

  # Validates that the string is a properly formatted email address
  email: EmailStr

  # Validates that the string is a valid URL
  linkedin_url: AnyUrl

  # Integer field with range constraints (greater than 0, less than 120)
  age: int = Field(gt=0, lt=120)

  # Float field that must be strictly greater than 0 (no type coercion for strict=True)
  weight: Annotated[float, Field(gt=0, strict=True)]

  # Boolean field indicating marital status, defaulting to None if not provided
  married: Annotated[
      Optional[bool], Field(default=None, description="Is the patient married or not")
  ]

  # Optional list of strings with a maximum limit of 5 items, defaulting to None
  allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]

  # Dictionary mapping string keys to string values for contact info
  contact_details: Dict[str, str]


# Function that takes a validated Patient model instance and prints its details
def update_patient_data(patient: Patient):
  print(patient.name)
  print(patient.age)
  print(patient.allergies)
  print(patient.married)
  print("updated")


# Raw dictionary containing patient information to be validated
patient_info = {
    "name": "nitish",
    "email": "abc@gmail.com",
    "linkedin_url": "http://linkedin.com/1322",
    "age": "30",  # Note: Pydantic automatically converts this string '30' into an integer
    "weight": 75.2,
    "contact_details": {"phone": "2353462"},
}

# Instantiate and validate the Patient model using unpacking (**)
patient1 = Patient(**patient_info)

# update_patient_data(patient1)  # Commented out as requested