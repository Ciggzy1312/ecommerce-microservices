from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from models.user import UserRegisterSchema
from services.user import registerUser

router = APIRouter(prefix="/user")

# Register User -> POST /api/user/register
@router.post("/register")
async def registerUserHandler(payload: UserRegisterSchema):
    if(payload.username == "" or payload.email == "" or payload.password == ""):
        return JSONResponse(status_code=400, content={"message": "Please fill all the fields"})

    user, error = await registerUser(payload.dict())
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=200, content={"message": "User registered successfully", "userId": str(user.inserted_id)})