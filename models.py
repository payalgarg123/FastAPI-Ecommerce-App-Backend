from tortoise import Model,fields
from pydantic import BaseModel
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator


class user(Model):
    id=fields.IntField(pk=True,index=True)
    username=fields.CharField(max_length=20,null=False,unique=True)
    email=fields.CharField(max_length=100,unique=True,null=False)
    password=fields.CharField(max_length=100,null=False)
    is_verified=fields.BooleanField(default=False)
    join_date=fields.DatetimeField(default=datetime.utcnow)



class Business(Model):
    id=fields.IntField(pk=True,index=True)
    business_name=fields.CharField(max_length=20,null=False,unique=True)
    city=fields.CharField(max_length=100,null=False,default="unsepicified")
    region=fields.CharField(max_length=100,null=False,default="unsepicified")
    business_des=fields.TextField(null=True)
    logo=fields.CharField(max_length=200,null=False,default="default.jpg")
    owner=fields.ForeignKeyField("models.user",related_name="business")



class Product(Model):
    id=fields.IntField(pk=True,index=True)
    name=fields.CharField(max_length=100,null=False,unique=True)
    category=fields.CharField(max_length=30,index=True)
    original_price=fields.DecimalField(max_digits=12,decimal_places=2)
    new_price=fields.DecimalField(max_digits=12,decimal_places=2)
    percentage_discount=fields.IntField()
    offer_expire_date=fields.DateField(default=datetime.utcnow)
    product_image=fields.CharField(max_length=200,null=False,default="default.jpg")
    date_published=fields.DatetimeField(default=datetime.utcnow)
    business=fields.ForeignKeyField("models.Business",related_name="product")



user_pydantic=pydantic_model_creator(user,name="user",exclude=("is_verified",))
user_pydanticIN=pydantic_model_creator(user,name="userIn",exclude_readonly=True,exclude=("is_verified","join_date"))
user_pydanticout=pydantic_model_creator(user,name="userOut",exclude=("password",))



Business_pydantic=pydantic_model_creator(Business,name="Business")
Business_pydanticIN=pydantic_model_creator(Business,name="BusinessIn",exclude=("logo","id"))


Product_pydantic=pydantic_model_creator(Product,name="Product")
product_pydanticIN=pydantic_model_creator(Product,name="ProductIn",exclude=("percentage_discount","id","product_image","date_published"))