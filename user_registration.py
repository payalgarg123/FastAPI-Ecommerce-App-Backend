from fastapi import FastAPI, HTTPException, Depends, status,APIRouter,Request
from models import *
from passlib.context import CryptContext




router = APIRouter(
    prefix='/register',
    tags=['register']
)


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def get_hashed_password(password):
    return bcrypt_context.hash(password)

@router.post("")
async def register_user(User:user_pydanticIN):
    user_info=User.dict(exclude_unset=True)
    user_info["password"]=get_hashed_password(user_info["password"])
    user_object=await user.create(**user_info)
    new_user=await user_pydantic.from_tortoise_orm(user_object)
    return { 
        "status":"ok","data":f"hello{new_user.username} , thanks for choosing your service check you email box you get the email verification, plaese verify your email"}