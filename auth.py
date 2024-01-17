from fastapi import FastAPI, HTTPException, Depends, status,APIRouter
from passlib.context import CryptContext




from dotenv import dotenv_values
import jwt
from models import *

from jose import jwt, JWTError
# import datetime
# from datetime import datetime
from datetime import datetime, timedelta

router=APIRouter()





config_credential=dotenv_values(".env")





# this function is verify your token
async def verify_token(token:str):
    try:
        payload=jwt.decode(token,config_credential["SECRET"],algorithms=["HS256"])
        User=await user.get(id=payload.get("id"))

    except:
        # print(f"Error decoding token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')
    return User


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


#verify password here we have two password one is plain password which u user created and converted password
async def verify_password(plain_password,hashed_password):
    return bcrypt_context.verify(plain_password,hashed_password)





async def authentic_user(username,password):
    User=await user.get(username=username)
    if User and verify_password(password,User.password):
        

        return User
    return False









async def token_generate(username:str,password:str):
    User=await authentic_user(username,password)
    if not User :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')
    
    token_data={
        "id":User.id,
        "username":User.username
    }
    expires= datetime.utcnow() + timedelta(minutes=30)  # Set your desired expiration time
    token_data.update({'exp': expires})
    token=jwt.encode(token_data,config_credential["SECRET"], algorithm="HS256")

    return token






