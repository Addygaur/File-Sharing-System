from pydantic import BaseModel


class Userschema(BaseModel):
    username:str
    password:str
