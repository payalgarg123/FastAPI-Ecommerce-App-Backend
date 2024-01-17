from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter, status
from pydantic import BaseModel, Field
from starlette import status
from models import *
from models import *
from auth import *
# from auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer






router = APIRouter()

ouath2_schema=OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def generate_token(request_form:OAuth2PasswordRequestForm=Depends()):
    token=await token_generate(request_form.username,request_form.password)
    return {"access_token":token,"token_type":"bearer"}




async def get_current_user(token:str=Depends(ouath2_schema)):
    try:
        payload=jwt.decode(token,config_credential["SECRET"],algorithms=["HS256"])
        User=await user.get(id=payload.get("id"))
        # if User is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')
    return await User 

@router.post("/user/me")
async def user_login(User:user_pydanticIN=Depends(get_current_user)):
    business=await Business.get(owner=User)
    logo=business.logo
    logo_path="localhost:8000/static/images/"+logo
    return {
        "status":"ok",
        "data":{
            "username":User.username,
            "email":User.email,
            "verified":User.is_verified,
            "join_date":User.join_date.strftime("%b %d %Y"),
            # "logo":logo_path
        }
    }