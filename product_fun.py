
from fastapi import File,UploadFile,APIRouter,Depends
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image
from models import *
from user_login import *

# router=APIRouter()
import image_processing
from image_processing import *

router=APIRouter()


@router.post("/uploadfile/product/{id}")
async def create_upload_file(id:int,file:UploadFile=File(...),User:user_pydantic=Depends(get_current_user)):
    filepath="./static/images"
    filename=file.filename
    #test.png
    extension=filename.split(".")[1]
    if extension not in ["png","jpg"]:
        return {"status":"error","detail":"file extension not allowed"}
    token_name=secrets.token_hex(10)+"."+extension
    generated_name=filepath+token_name
    file_content =await file.read()

    with open(generated_name,"wb") as file:
        file.write(file_content)

    img=Image.open(generated_name)
    img=img.resize(size=(200,200))
    img.save(generated_name)
    file.close()
    product=await Product.get(id=id)
    business=await product.business
    owner=await business.owner
    if owner==User:
        product.product_image=token_name
        await product.save()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')
    return{"status":"ok","filename":"file is succesfully uploaded"}


#crud
@router.post("/product")
async def add_new_product(product:product_pydanticIN,User:user_pydantic=Depends(get_current_user)):
    product=product.dict(exclude_unset=True)
    # Create a Business object before creating the Product object
    business_obj = await Business.create(business_name="Some Business Name", owner=User)
    #to avoid division error by zero
    if product["original_price"]>0:
        product["percentage_discount"]=((product["original_price"]-product["new_price"])/product["original_price"])*100
        product_obj=await Product.create(**product,business=business_obj)
        product_obj=await Product_pydantic.from_tortoise_orm(product_obj)

        return {"status":"ok","data":product_obj}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid user')
    

@router.get("/product")
async def get_product():
    response= await Product_pydantic.from_queryset(Product.all())
    return {"status":"ok","data":response}

@router.get("/{id}")
async def get_product(id:int):
    product= await Product.get(id=id)
    business=await product.business
    owner=await business.owner
    response=await Product_pydantic.from_queryset_single(Product.get(id=id))
    return {"status":"ok","data":{
        "product_details":response,
        "business_details":{
            "name":business.business_name,
            "city":business.city,
            "region":business.region,
            "business_des":business.business_des,
            "logo":business.logo,
            "owner_id":business.id,
            "email":business.email,
            "join_date":business.join_date.strftime("%b %d %Y")
        }
    }}


@router.delete("/product/{id}")
async def delete_product(id:int,User:user_pydantic=Depends(get_current_user)):
    product=await Product.get(id=id)
    business=await product.business
    owner= await business.owner
    if User==owner:
        product.delete()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')
    return {"status":"ok"}


@router.put("/product/{id}")
async def update_product(id:int,update_info:product_pydanticIN,User:user_pydantic=Depends(get_current_user)):
    product=await Product.get(id=id)
    business=await product.business
    owner=await business.owner

    update_info=update_info.dict(exclude_unset=True)
    update_info["date_published"]=datetime.utcnow
    if User==owner and update_info["original_price"] >0:
        product["percentage_discount"]=((product["original_price"]-product["new_price"])/product["original_price"])*100
        product=await product.update_from_dict(update_info)
        product.save()
        response=await Product_pydantic.from_tortoise_orm(product)
        return{"status":"ok","data":response}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')



