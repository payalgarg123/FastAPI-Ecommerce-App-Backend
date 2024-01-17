from fastapi import FastAPI
from models import *
from tortoise import models
from tortoise.contrib.fastapi import register_tortoise
from email_sender import send_email
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
import user_registration
import user_verification
import auth
import user_login,image_processing,product_fun
app=FastAPI()

@post_save(user)
async def create_business(
    sender:"Type[user]",
    instance:user,
    created:bool,
    using_db:"Optional[BaseDBAsyncClient]",
    update_fields:List[str]
) -> None:
    if created:
        business_object=await Business.create(
            business_name=instance.username,owner=instance
        )
        await Business_pydantic.from_tortoise_orm(business_object)
        # send_the_email
        await send_email([instance.email],instance)

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models":["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)

app.include_router(user_registration.router)
app.include_router(user_verification.router)
app.include_router(auth.router)
app.include_router(user_login.router)
app.include_router(image_processing.router)
app.include_router(product_fun.router)




