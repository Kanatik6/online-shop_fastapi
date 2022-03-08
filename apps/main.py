from fastapi import FastAPI
from database import engine, Base
from decouple import config
from products.routers import router as router_product

from users.routers import router as router_user

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Shop")

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


app.include_router(router=router_product)
app.include_router(router=router_user)
