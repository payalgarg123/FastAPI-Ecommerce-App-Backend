from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth import verify_token
from models import user, Business, Business_pydantic
from email_sender import send_email


router=APIRouter(prefix='/verification',
    tags=['verification'])






templates=Jinja2Templates(directory="templates")
@router.get("",response_class=HTMLResponse)
async def email_verification(request:Request,token:str):
    User=await verify_token(token)

    if User and not User.is_verified:
        User.is_verified=True
        await User.save()
        return templates.TemplateResponse("verification.html",{"request":request,"username":User.username})
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')


