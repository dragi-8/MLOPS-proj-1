import sys
from src.entity.config_entity import Vehiclepredictorconfig
from src.entity.s3_estimator import Proj1Estimator
from src.exception import MYexception
from src.logger import logging
from pandas import DataFrame


class vehicledata:
    def __init__(self,
                 Gender,Age,
  Driving_License,
  Region_Code,
  Previously_Insured,
Vehicle_Age_gt_2_Years,Vehicle_Age_lt_1_Year,
  Vehicle_Damage_Yes,
   Annual_Premium,
   Policy_Sales_Channel,
   Vintage):
        try:
            self.Gender=Gender
            self.Age=Age
            self.Driving_License=Driving_License
            self.Region_Code=Region_Code
            self.Previously_Insured=Previously_Insured
            self.Vehicle_Age_gt_2_Years=Vehicle_Age_gt_2_Years
            self.Vehicle_Age_lt_1_Year=Vehicle_Age_lt_1_Year
            self.Vehicle_Damage_Yes=Vehicle_Damage_Yes
            self.Annual_Premium=Annual_Premium
            self.Policy_Sales_Channel=Policy_Sales_Channel
            self.Vintage=Vintage
        except Exception as e:
            raise MYexception(e, sys)
        
    def get_vehicle_data_as_dict(self):
        try:
            input_data={
                    "Gender": [self.Gender],
                    "Age": [self.Age],
                    "Driving_License": [self.Driving_License],
                    "Region_Code": [self.Region_Code],
                    "Previously_Insured": [self.Previously_Insured],
                    "Vehicle_Age_gt_2_Years": [self.Vehicle_Age_gt_2_Years],
                    "Vehicle_Age_lt_1_Year": [self.Vehicle_Age_lt_1_Year],
                    "Vehicle_Damage_Yes": [self.Vehicle_Damage_Yes],
                    "Annual_Premium": [self.Annual_Premium],
                    "Policy_Sales_Channel": [self.Policy_Sales_Channel],
                    "Vintage": [self.Vintage]
                }
            return input_data
        except Exception as e:
            raise MYexception(e, sys)
        
    def get_vehicle_data_as_dataframe(self):
        try:
            data = self.get_vehicle_data_as_dict()
            return DataFrame(data)
        except Exception as e:
            raise MYexception(e, sys)
        
class Vehicleclassifier:
    def __init__(self,pipeline_predictor_config:Vehiclepredictorconfig=Vehiclepredictorconfig()):
        try:
            self.pipeline_predictor_config=pipeline_predictor_config

        except Exception as e:
            raise MYexception(e, sys)

    def predict(self, dataframe:DataFrame):
        try:
            logging.info('starting prediction using vehicle classifier')
            model=Proj1Estimator(model_bucket_name=self.pipeline_predictor_config.model_bucket_name, model_key_path=self.pipeline_predictor_config.model_key_path) 

            return model.predict(dataframe)
        except Exception as e:
            raise MYexception(e, sys)