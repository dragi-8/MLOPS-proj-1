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

     
# @dataclass
# class Datatransformationartifact: 

# @dataclass
# class Datavalidationartifact: