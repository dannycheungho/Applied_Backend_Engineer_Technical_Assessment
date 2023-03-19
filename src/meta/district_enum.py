from enum import Enum
 
class DistrictEnum(Enum):
    def __new__(cls, English, Chinese):
        obj = object.__new__(cls)
        obj.English = English
        obj.Chinese = Chinese
        return obj
        
    Hong_Kong_Island = ('HONG KONG ISLAND', '香港島')
    Kowloon= ('KOWLOON','九龍')
    New_Territories = ('NEW TERRITORIES','新界')

