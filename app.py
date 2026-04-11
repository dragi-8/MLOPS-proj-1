from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run
from src.exception import MYexception
import sys
from typing import Optional

# Importing constants and pipeline modules from the project
from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import vehicledata, Vehicleclassifier
from src.pipline.training_pipeline import Trainpipeline

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates=Jinja2Templates(directory="templates")

origins=["*"]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

class Dataform:
    def __init(self,request:Request):
        self.request=request
        self.Gender: Optional[str]=None
        self.Age: Optional[int]=None    
        self.Driving_License: Optional[int]=None
        self.Region_Code: Optional[float]=None
        self.Previously_Insured: Optional[int]=None
        self.Vehicle_Age_gt_2_Years: Optional[int]=None
        self.Vehicle_Age_lt_1_Year: Optional[int]=None
        self.Vehicle_Damage_Yes: Optional[int]=None
        self.Annual_Premium: Optional[float]=None
        self.Policy_Sales_Channel: Optional[float]=None
        self.Vintage: Optional[int]=None

    async def get_vehicle_data(self):
        form=await self.request.form()
        self.Gender=form.get('Gender')
        self.Age=form.get('Age')
        self.Driving_License=form.get('Driving_License')
        self.Region_Code=form.get('Region_Code')
        self.Previously_Insured=form.get('Previously_Insured')
        self.Vehicle_Age_gt_2_Years=form.get('Vehicle_Age_gt_2_Years')
        self.Vehicle_Age_lt_1_Year=form.get('Vehicle_Age_lt_1_Year')
        self.Vehicle_Damage_Yes=form.get('Vehicle_Damage_Yes')
        self.Annual_Premium=form.get('Annual_Premium')
        self.Policy_Sales_Channel=form.get('Policy_Sales_Channel')
        self.Vintage=form.get('Vintage')

@app.get('/',tags=['authentication']) 
async def index(request:Request):
    return templates.TemplateResponse('index.html',{"request":request,'context':'rendering'}) 

@app.get("/train")
async def train_route():
    try:
        train_pipeline=Trainpipeline()
        train_pipeline.run_pipeline()
        return Response(content="training successful", media_type="text/plain")
    except Exception as e:
        raise MYexception(e,sys) 

@app.post('/')     
async def predict_route(request:Request):
    try:
        form=Dataform(request)
        await form.get_vehicle_data()
        vehicle_data=vehicledata( Gender=form.Gender, Age=form.Age, Driving_License=form.Driving_License, Region_Code=form.Region_Code, Previously_Insured=form.Previously_Insured, Vehicle_Age_gt_2_Years=form.Vehicle_Age_gt_2_Years, Vehicle_Age_lt_1_Year=form.Vehicle_Age_lt_1_Year, Vehicle_Damage_Yes=form.Vehicle_Damage_Yes, Annual_Premium=form.Annual_Premium, Policy_Sales_Channel=form.Policy_Sales_Channel, Vintage=form.Vintage )

        vehicle_df=vehicle_data.get_vehicle_data_as_dataframe()
        model_predictor=Vehicleclassifier()
        value=model_predictor.predict(vehicle_df)[0]
        status='yes' if value[0]==1 else 'no'
        return templates.TemplateResponse('index.html',{"request":request,'context':status})
    except Exception as e:
        raise MYexception(e,sys)


if __name__=="__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)