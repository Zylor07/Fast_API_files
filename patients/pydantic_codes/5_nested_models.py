from pydantic import BaseModel


class Address(BaseModel):

  city: str
  state: str
  pin: str


class Patient(BaseModel):

  name: str
  gender: str
  age: int
  # Nested Model: Embedding the Address model inside the Patient model for better organization
  address: Address


# Dictionary representing address data
address_dict = {"city": "gurgaon", "state": "haryana", "pin": "122001"}

# Instantiate the nested Address model first
address1 = Address(**address_dict)

# Dictionary representing patient data, referencing the instantiated Address model
patient_dict = {"name": "nitish", "gender": "male", "age": 35, "address": address1}

# Instantiate the main Patient model (Nested validation happens automatically here)
patient1 = Patient(**patient_dict)

# Syntax usage: model_dump(include=...) serializes the model to a dictionary while filtering fields.
# Using '...' (Ellipsis) tells Pydantic to include the entire field or nested keys.
temp = patient1.model_dump(include={"name": ..., "address": {"city": ...}})

print(temp)
print(type(temp))

# --- Benefits of Nested Models ---
# 1. Better organization of related data (e.g., vitals, address, insurance)
# 2. Reusability: Use Address or Vitals in multiple models (e.g., Patient, MedicalRecord)
# 3. Readability: Easier for developers and API consumers to understand
# 4. Validation: Nested models are validated automatically—no extra work needed