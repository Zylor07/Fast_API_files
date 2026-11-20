from pydantic import BaseModel


class Address(BaseModel):

  city: str
  state: str
  pin: str


class Patient(BaseModel):

  name: str
  gender: str = "Male"  # Default value specified here
  age: int
  address: Address


# Dictionary representing address data
address_dict = {"city": "gurgaon", "state": "haryana", "pin": "122001"}

# Instantiate the nested Address model
address1 = Address(**address_dict)

# Dictionary representing patient data.
# Notice that 'gender' is omitted here to demonstrate how exclude_unset works.
patient_dict = {"name": "nitish", "age": 35, "address": address1}

# Instantiate the main Patient model
patient1 = Patient(**patient_dict)

# --- SERIALIZATION EXAMPLES & SYNTAX USAGE ---

# 1. exclude_unset=True Usage & Syntax:
# Tells Pydantic to only include fields that were explicitly provided during initialization,
# ignoring fields that fell back to their default values (like 'gender').
temp_unset = patient1.model_dump(exclude_unset=True)
print("exclude_unset=True output:", temp_unset)
print(type(temp_unset))

print("-" * 40)

# 2. model_dump() (Standard Dictionary Serialization):
# Converts the model into a standard Python dictionary, including all fields (explicit and default).
full_dict = patient1.model_dump()
print("Full model_dump() output:", full_dict)

print("-" * 40)

# 3. exclude=... Usage & Syntax:
# Specifies fields or nested attributes to drop from the final output.
# Here we exclude 'age' at the root level, and 'pin' inside the nested 'address' model.
excluded_data = patient1.model_dump(exclude={"age":..., "address": {"pin":...}})
print("model_dump with exclude output:", excluded_data)

print("-" * 40)

# 4. model_dump_json() Usage & Syntax:
# Serializes the model directly into a valid JSON string (useful for API responses).
# Supports the same arguments like indent for pretty printing.
json_string = patient1.model_dump_json(indent=2)
print("model_dump_json() string output:\n", json_string)
print("Type:", type(json_string))