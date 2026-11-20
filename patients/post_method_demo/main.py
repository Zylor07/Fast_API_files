from typing import Annotated, Literal
import json
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

app = FastAPI()


# --- Pydantic Model for Patient Validation & Request Body ---
class Patient(BaseModel):
  id: Annotated[
      str, Field(..., description="ID of the patient", examples=["P001"])
  ]
  name: Annotated[str, Field(..., description="Name of the patient")]
  city: Annotated[str, Field(..., description="City where the patient is living")]
  age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
  gender: Annotated[ Literal["male", "female", "others"],Field(..., description="Gender of the patient"),]
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


# --- POST Request Endpoint Implementation ---


@app.post("/create")
def create_patient(patient: Patient):
  """Syntax usage:

  1. Request Body: FastAPI automatically reads incoming JSON from the client request
     and validates it against the `Patient` Pydantic model.
  2. data[patient.id]: Uses the patient's ID as the primary key dictionary lookup.
  3. model_dump(exclude=['id']): Serializes the Pydantic model into a dictionary
     while omitting the 'id' field since it is already used as the dictionary key.
  4. JSONResponse: Allows returning custom HTTP status codes (like 201 Created).
  """
  # 1. Load existing database records from demo_patients-v2.json
  data = load_data()

  # 2. Check if the patient already exists to prevent duplicate entries
  if patient.id in data:
    raise HTTPException(status_code=400, detail="Patient already exists")

  # 3. Add the new patient to the database dictionary (excluding redundant 'id' inside values)
  data[patient.id] = patient.model_dump(exclude=["id"])

  # 4. Save the updated database dictionary back into demo_patients-v2.json
  save_data(data)

  # 5. Return success response with HTTP status code 201 (Created)
  return JSONResponse(
      status_code=201, content={"message": "patient created successfully"}
  )