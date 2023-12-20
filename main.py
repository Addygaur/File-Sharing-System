import uvicorn
from fastapi import (
    FastAPI, Body, UploadFile, Depends, HTTPException, JSONResponse
)
from dto.login_dto import UserSchema
from dto.signup_dto import SignupRequest
from dto.token_dto import Token
from usecase.ops.add_resource import add_resource_usecase
from usecase.ops.ops_signup import ops_signup_usecase
from usecase.users.get_all_resource import get_all_resource_usecase
from usecase.users.get_resource import get_resource_usecase
from usecase.users.user_signup import user_signup_usecase
from utils.authentication import authenticate_user
from utils.authorization import jwtBearer
from utils.role import RoleChecker

app = FastAPI()

# Routes
@app.post("/login", response_model=Token)
async def login(form_data: UserSchema = Body()):
    token = await authenticate_user(form_data)
    return token

@app.post("/admin/signup", tags=['admin'])
async def signup(request: SignupRequest):
    data = await ops_signup_usecase(request)
    return JSONResponse(
        status_code=data["status"],
        content=data["message"]
    )

@app.post("/admin/uploadfile", tags=['admin'], dependencies=[Depends(jwtBearer()), Depends(RoleChecker(["admin"]))])
async def upload_file(file: UploadFile):
    upload_result = await add_resource_usecase(file)
    if upload_result:
        return JSONResponse(status_code=200, content=upload_result)
    else:
        raise HTTPException(status_code=500, detail="Failed to upload file")

@app.post("/user/signup", tags=['user'])
async def signup(request: SignupRequest):
    data = await user_signup_usecase(request)
    return JSONResponse(
        status_code=data["status"],
        content=data["message"]
    )

@app.get("/getfile", tags=['user'], dependencies=[Depends(jwtBearer()), Depends(RoleChecker(["admin", "user"]))])
async def get_file(file_name: str):
    data = await get_resource_usecase(file_name)
    if data:
        return JSONResponse(status_code=200, content={"message": "File fetched successfully", "url": f'{data}'})
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch file")

@app.get("/list-file", tags=['user'], dependencies=[Depends(jwtBearer()), Depends(RoleChecker(["admin", "user"]))])
async def get_files():
    data = await get_all_resource_usecase()
    if data:
        return JSONResponse(status_code=200, content={"message": "Files fetched successfully", "Files": f'{data}'})
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch files")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
