from pymongo import MongoClient 
from pymongo import*
import datetime
from camera import Camera




class DataManger():
    client=MongoClient("localhost",27017)
    db=client["raspFlir"]
    collect=db["tempture"]

    def __init__ (self):
        pass
        
    @classmethod
    def save(cls,temperatureData):
        
        data={
            "class":1,
            "date":datetime.datetime.now().isoformat(),
            "temperature":temperatureData
        }
        
        cls.collect.insert(data)

    @classmethod
    def find(cls,requset):
        
        return cls.collect.find(requset)
       