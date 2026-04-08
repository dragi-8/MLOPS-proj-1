from dataclasses import dataclass

@dataclass
class Dataingestionartifact:
    train_file_path:str
    test_file_path:str

@dataclass
class Datavalidationartifact:
    validation_error_msg:str
    report_file_path:str
    validation_condition:bool   

     
@dataclass
class Datatransformationartifact: 
    transformed_train_file_path:str
    transformed_test_file_path:str
    transformed_object_path:str

@dataclass
class Metricartifact:
    f1_score:float
    recall_score:float
    precision_score:float
@dataclass
class Modeltrainerartifact:
    model_file:str
    metric:Metricartifact