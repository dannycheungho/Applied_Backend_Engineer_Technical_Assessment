from enum import Enum
 
class CategoryEnum(Enum):
    def __new__(cls, English, Chinese):
        obj = object.__new__(cls)
        obj.English = English
        obj.Chinese = Chinese
        return obj
    General_Practitioner = ('General Practitioner','普通科門診')
    Epidemiologist = ('Epidemiologist', '流行病')