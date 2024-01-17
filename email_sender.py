from fastapi.background import BackgroundTasks
import smtplib
from fastapi import FastAPI, HTTPException, Depends, status,APIRouter,Request
from fastapi_mail import  FastMail,MessageSchema,ConnectionConfig
from dotenv import dotenv_values
from pydantic import BaseModel,EmailStr
from typing import List
from models import *
import jwt


config_credentials=dotenv_values(".env")



conf=ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    # Add these fields if required
      # Add these fields if required
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


class Email_schema(BaseModel):
    email:List[EmailStr]



async def send_email(email:List,instance:user):
    token_data={
        "id":instance.id,
        "username":instance.username
    }
    token=jwt.encode(token_data,config_credentials["SECRET"],algorithm="HS256")
    template=f"""  
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
    <div style="display: flex;align-items:center;justify-content:center;flex-direction:column">
    <h3>Account Verification </h3>
    <br>
    <p>thanks for choosing nykaa, please click on the button to verify</p>
    <a style="margin-top:1rem;padding: 1rem;border-radius:0.5rem;font-size:1rem;
    text-decoration:none;background:blue;color:white;" href="http://localhost:8000/verification/?token={token}">verify</a>
    <p> please kindly ignore this email if you did not register for nykaa and nothing will happened</p>
    </div>
    </body>



    </html>"""
    message=MessageSchema(
        subject="nykaa account verification email",
        recipients=email,#list of email
        body=template,
        subtype="html"
    )



    fm=FastMail(conf)
    await fm.send_message(message=message)