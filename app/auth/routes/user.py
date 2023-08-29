from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from bson import ObjectId

from models.user import UserRegisterSchema, UserLoginSchema
from services.user import registerUser, loginUser, getCurrentUser
from dependency import get_current_user

router = APIRouter(prefix="/user")

# Register User -> POST /api/user/register
@router.post("/register")
async def registerUserHandler(payload: UserRegisterSchema):
    if(payload.username == "" or payload.email == "" or payload.password == ""):
        return JSONResponse(status_code=400, content={"message": "Please fill all the fields"})

    user, error = await registerUser(payload.dict())
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=201, content={"message": "User registered successfully", "userId": str(user.inserted_id)})


# Login User -> POST /api/auth/login
@router.post("/login")
async def loginUserHandler(payload: UserLoginSchema):
    if payload.email == "" or payload.password == "":
        return JSONResponse(status_code=400, content={"message": "Please fill all the fields"})

    token, error = await loginUser(payload.dict())
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    template_response = JSONResponse(status_code=200, content={"message": "User logged in successfully", "token": token})
    template_response.set_cookie(key="token", value=token, httponly=True)

    return template_response


# Get User Profile Details -> GET /api/user/me
@router.get("/me")
async def getCurrentUserHandler(payload: dict = Depends(get_current_user)):
    user, error = await getCurrentUser(payload)
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=200, content={"message": "User details fetched successfully", "user": user})