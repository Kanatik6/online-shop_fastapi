from pydantic import BaseModel, Field

class User(BaseModel):
    first_name: str = Field(...,min_length=5,max_length=20)
    last_name: str = Field(...,min_length=5,max_length=20)
    password:str = Field(...,min_length=5,max_length=100)

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    first_name:str = Field(...,min_length=5,max_length=20)
    password:str = Field(...,min_length=5,max_length=100)
    
    class Config:
        orm_mode = True


class ReturnUser(BaseModel):
    id:int
    first_name:str
    last_name:str
    
    class Config:
        orm_mode = True


class Post(BaseModel):
    title: str = Field(...,min_length=3,max_length=40)
    descriptions: str = Field(...,min_length=3,max_length=1000)
    
    class Config:
        orm_mode = True

class ReturnPost(BaseModel):
    id:int
    title:str
    descriptions:str

    class Config:
        orm_mode = True
