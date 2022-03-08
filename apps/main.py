from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine,Base
from users.auth.jwt_bearer import JWTBearer
from users.auth.jwt_bearer import get_current_user
from decouple import config
from products.routers import router as router_product
from products.crud import create_cart


from users import schemas,models,crud
from database import get_db

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Shop")

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


app.include_router(router=router_product)




@app.get('/post/',response_model=list[schemas.ReturnPost],tags=['post'])
def get_list_post(db:Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get('/post/{id}',response_model=schemas.ReturnPost,tags=['post'])
def get_detail_post(*,db:Session= Depends(get_db),id:int):
    post = db.query(models.Post).filter_by(id=id).first()
    return post


@app.post('/post/',dependencies=[Depends(JWTBearer())],response_model=schemas.ReturnPost,tags=['post'])
def create_post(*,db:Session= Depends(get_db),post:schemas.Post,user:dict=Depends(get_current_user)):
    post = models.Post(title=post.title,descriptions=post.descriptions)
    print(user)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# --

@app.post('/user/sing-up/',response_model=schemas.ReturnUser,tags=['user'])
def create_user(*,db:Session= Depends(get_db),user:schemas.User):
    user = crud.create_user(db=db,user=user)
    create_cart(db=db,id=user.id)
    return user

@app.post('/user/sing-in/',tags=['user'])
def login_user(*,db:Session = Depends(get_db),user:schemas.UserLogin,tags=['user']):
    return crud.login_user(db=db,user=user)
