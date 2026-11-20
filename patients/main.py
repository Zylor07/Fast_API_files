from fastapi import FastAPI,Path,HTTPException,Query
import json
app=FastAPI()
def load_data():
    with open('demo_patients-v2.json','r') as f:
        data=json.load(f)

    return data

@app.get("/")
def read_root():
    return{'message':'Patient management system'}
@app.get("/about")
def about():
    return{'message':'This a fully functional API'}

@app.get("/view")
def call_the_json():
    data=load_data()

    return data

@app.get('/patient/{patient_id}') #created a patient id hitting url
def view_patient(patient_id:str=Path(...,description='id of the patient in json',example='P001')): #patient_id is a variable created . because of in json the patient id is string so variable assigned with stirng
    #and here path is a function which is used to provide metadata,validation rules and documentation hints for path parameters in your API endpoints 
 #.... is used for telling that this field is required(must)
    data= load_data() #loaded the whole json data 

    if patient_id in data:    #if else statement to find the patient id and return 
        return data[patient_id]
    raise HTTPException(status_code=404,detail='patient not found') #handiling not found with http code
   # return {'patient not found'}

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='sort on the basis of height , weight and bmi '),order:str=Query('asc',description='sort in the asc or desc order')):
    vaild_fields=['height','weight','bmi']
    if sort_by not in vaild_fields:
        raise HTTPException(status_code=400,detail='bad request form client side choose correct values {vaild_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='choose between asc or desc order ')
    
    data=load_data()

    sort_order=True if order=='desc' else False

    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data
    
     

