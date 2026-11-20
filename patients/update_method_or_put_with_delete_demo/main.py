from typing import Annotated, Literal, Optional
import json
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

app = FastAPI()


# --- Pydantic Model for Patient Creation ---
class Patient(BaseModel):
  id: Annotated[
      str, Field(..., description="ID of the patient", examples=["P001"])
  ]
  name: Annotated[str, Field(..., description="Name of the patient")]
  city: Annotated[str, Field(..., description="City where the patient is living")]
  age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
  gender: Annotated[
      Literal["male", "female", "others"],
      Field(..., description="Gender of the patient"),
  ]
  height: Annotated[
      float, Field(..., gt=0, description="Height of the patient in mtrs")
  ]
  weight: Annotated[
      float, Field(..., gt=0, description="Weight of the patient in kgs")
  ]

  # Computed field syntax usage: Automatically calculates BMI based on weight and height
  @computed_field
  @property
  def bmi(self) -> float:
    return round(self.weight / (self.height**2), 2)

  # Computed field syntax usage: Automatically categorizes health status based on BMI
  @computed_field
  @property
  def verdict(self) -> str:
    if self.bmi < 18.5:
      return "Underweight"
    elif self.bmi < 25:
      return "Normal"
    elif self.bmi < 30:
      return "Overweight"
    else:
      return "Obese"


# --- Pydantic Model for Patient Updates (Partial Updates) ---
class PatientUpdate(BaseModel):
  # Syntax usage: Optional with default=None allows clients to pass only the fields they want to update
  name: Annotated[Optional[str], Field(default=None)]
  city: Annotated[Optional[str], Field(default=None)]
  age: Annotated[Optional[int], Field(default=None, gt=0)]
  gender: Annotated[Optional[Literal["male", "female", "others"]], Field(default=None)]
  height: Annotated[Optional[float], Field(default=None, gt=0)]
  weight: Annotated[Optional[float], Field(default=None, gt=0)]


# --- Helper Functions for File I/O ---


def load_data():
  """Syntax usage: Opens and reads patient data from 'demo_patients-v2.json'."""
  with open("demo_patients-v2.json", "r") as f:
    data = json.load(f)
  return data


def save_data(data):
  """Syntax usage: Writes/saves updated patient data back to 'demo_patients-v2.json'."""
  with open("demo_patients-v2.json", "w") as f:
    json.dump(data, f, indent=4)


# --- API Endpoints ---


@app.get("/")
def read_root():
  return {"message": "Patient Management System API"}


@app.get("/view")
def call_the_json():
  data = load_data()
  return data


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ..., description="id of the patient in json", example="P001"
    )
):
  data = load_data()
  if patient_id in data:
    return data[patient_id]
  raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ..., description="sort on the basis of height , weight and bmi "
    ),
    order: str = Query("asc", description="sort in the asc or desc order"),
):
  valid_fields = ["height", "weight", "bmi"]
  if sort_by not in valid_fields:
    raise HTTPException(
        status_code=400,
        detail=f"Bad request from client side. Choose correct values: {valid_fields}",
    )
  if order not in ["asc", "desc"]:
    raise HTTPException(
        status_code=400, detail="Choose between asc or desc order"
    )

  data = load_data()
  sort_order = True if order == "desc" else False
  sorted_data = sorted(
      data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order
  )
  return sorted_data


# --- POST Request Endpoint ---


@app.post("/create")
def create_patient(patient: Patient):
  """Syntax usage:

  1. Request Body: FastAPI reads and validates client JSON against the `Patient` model.
  2. model_dump(exclude=['id']): Serializes model to dictionary without the 'id' field.
  """
  data = load_data()

  if patient.id in data:
    raise HTTPException(status_code=400, detail="Patient already exists")

  data[patient.id] = patient.model_dump(exclude=["id"])
  save_data(data)

  return JSONResponse(
      status_code=201, content={"message": "patient created successfully"}
  )


# --- PUT Request Endpoint (Update Feature) ---


@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
  """Syntax usage:

  1. patient_id: Path parameter to identify which patient to update.
  2. patient_update: Request body validated against `PatientUpdate` (all fields optional).
  3. exclude_unset=True: Only extracts fields that the client explicitly sent in the request.
  4. Dynamic merging: Iterates through updated keys to modify only specified attributes.
  """
  data = load_data()

  # 1. Check if patient exists in database
  if patient_id not in data:
    raise HTTPException(status_code=404, detail="Patient not found")

  # 2. Grab existing patient record dictionary from json database
  existing_patient_info = data[patient_id]

  # 3. Dump only the fields that were actually provided by the client request
  updated_patient_info = patient_update.model_dump(exclude_unset=True)

  # 4. Merge incoming changes into the existing record dictionary
  for key, value in updated_patient_info.items():
    existing_patient_info[key] = value

  # 5. Conversion flow logic (commented properly):
  #    existing_patient_info (dict) -> Pydantic object (Patient) -> updates bmi + verdict
  #    -> Pydantic object -> model_dump() (dict)
  updated_patient_obj = Patient(id=patient_id, **existing_patient_info)
  data[patient_id] = updated_patient_obj.model_dump(exclude=["id"])

  # 6. Save updated record back to database file
  save_data(data)

  return JSONResponse(status_code=200, content={"message": "patient updated"})


# --- DELETE Request Endpoint (Delete Feature) ---[cite: 16, 17]


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
  """Syntax usage:

  1. @app.delete: FastAPI decorator specifying a DELETE HTTP method route.
  2. patient_id: Path parameter used to locate the specific record in JSON.
  3. del data[patient_id]: Standard Python dictionary keyword to delete a key-value pair.
  4. save_data(data): Persists the deletion back to the JSON storage file.
  """
  # 1. Load existing database records[cite: 16, 17]
  data = load_data()

  # 2. Validate if the patient exists before attempting deletion[cite: 16, 17]
  if patient_id not in data:
    raise HTTPException(status_code=404, detail="Patient not found")

  # 3. Delete the patient record key from the dictionary[cite: 16, 17]
  del data[patient_id]

  # 4. Save the modified database back to json storage[cite: 17]
  save_data(data)

  # 5. Return success response[cite: 17]
  return JSONResponse(status_code=200, content={"message": "patient deleted"})