from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine,Base
from users.auth.jwt_bearer import JWTBearer
from products.routers import get_products 

from users import schemas,models,crud

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Shop")


# app.include_router(router=product_router)

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@app.get('/post/',response_model=list[schemas.ReturnPost],tags=['post'])
def get_list_post(db:Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get('/post/{id}',response_model=schemas.ReturnPost,tags=['post'])
def get_detail_post(*,db:Session= Depends(get_db),id:int):
    post = db.query(models.Post).filter_by(id=id).first()
    return post


@app.post('/post/',dependencies=[Depends(JWTBearer())],response_model=schemas.ReturnPost,tags=['post'])
def create_post(*,db:Session= Depends(get_db),post:schemas.Post):
    post = models.Post(title=post.title,descriptions=post.descriptions)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# --

@app.post('/user/sing-up/',response_model=schemas.ReturnUser,tags=['user'])
def create_user(*,db:Session= Depends(get_db),user:schemas.User):
    user = crud.create_user(db=db,user=user)
    return user

@app.post('/user/sing-in/',tags=['user'])
def login_user(*,db:Session = Depends(get_db),user:schemas.UserLogin,tags=['user']):
    return crud.login_user(db=db,user=user)
