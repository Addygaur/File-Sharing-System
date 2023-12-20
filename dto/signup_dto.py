from pydantic import BaseModel
from pydantic import BaseModel

class signup_request(BaseModel):
    first_name : str
    last_name : str
    email : str
    password : str
