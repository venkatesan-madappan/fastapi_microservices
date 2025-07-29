from pydantic_settings import BaseSettings
from datetime import date
import os

class FacultySettings(BaseSettings): 
    application:str = 'Faculty Management System' 
    webmaster:str = 'vm@university.com'
    created:date = '2025-07-24'

class LibrarySettings(BaseSettings): 
    application:str = 'Library Management System' 
    webmaster:str = 'vm@university.com'
    created:date = '2025-07-24'
 

class StudentSettings(BaseSettings): 
    application:str = 'Student Management System' 
    webmaster:str = 'vm@university.com'
    created:date = '2025-07-24'

    
class ServerSettings(BaseSettings): 
    production_server:str
    prod_port:int
    development_server:str 
    dev_port:int
    
    class Config: 
        env_file = os.getcwd() + '/configuration/erp_settings.properties'
        

    
    