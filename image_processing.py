from fastapi import File,UploadFile,APIRouter,Depends
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image
from models import *
from user_login import *
from auth import *

router=APIRouter()

#file setup
router.mount("/static",StaticFiles(directory="static"),name="static")



@router.post("/uploadfile/profile")
async def create_upload_file(file:UploadFile=File(...),User:user_pydantic=Depends(get_current_user)):
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
    business=await Business.get(owner=User)
    owner=await business.owner
    if owner==User:
        business.logo=token_name
        await business.save()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')
    return{"status":"ok","filename":"file is succesfully uploaded"}



# @router.put("/business/{id}")
# async def update_product(id:int,update_business:Business_pydanticIN,User:user_pydantic=Depends(get_current_user)):
#     update_business=update_business.dict()
#     business=await Business.get(id=id)
#     business_owner=await business.owner
#     if User==business_owner:
#         await business.update_from_dict(update_business)
#         business.save()
#         response=await Business_pydantic.from_tortoise_orm(business)
#         return{"status":"ok","data":response}
#     else:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')
@router.put("/business/{id}")
async def update_product(id: int, update_business: Business_pydanticIN, User: user_pydantic = Depends(get_current_user)):
    update_business = update_business.dict()

    # Check if the Business object exists
    business = await Business.filter(id=id).first()
    
    if business:
        business_owner = await business.owner

        if User == business_owner:
            # Update the Business object directly
            business.business_name = update_business.get('business_name', business.business_name)
            business.city = update_business.get('city', business.city)
            business.region = update_business.get('region', business.region)
            business.business_des = update_business.get('business_des', business.business_des)
            business.logo = update_business.get('logo', business.logo)
            await business.save()

            response = await Business_pydantic.from_tortoise_orm(business)
            return {"status": "ok", "data": response}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!!')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Business not found')