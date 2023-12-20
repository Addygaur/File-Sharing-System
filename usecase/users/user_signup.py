import sqlite3

from fastapi import HTTPException

from config import USER_DATABASE
from database.userdatastore import UserDataStore
from dto.signup_dto import signup_request
from entity.user import user_info, Role


async def user_signup_usecase(request: signup_request):
    payload=user_info(
                    first_name = request.first_name,
                    last_name=request.last_name,
                    email=request.email,
                    password=request.password,
                    role=Role.USER.value
    )
    with sqlite3.connect(USER_DATABASE) as conn :
        repo = UserDataStore(conn)
        check = await repo.check_email_id(email_id=request.email)
        if not check :
            data=await repo.create_user(payload)
            return {
                "status":200,
                "message": "User Created Successfull"
            }

        else:
            return {
                "status":403,
                "message": "User with same email id present"
            }
