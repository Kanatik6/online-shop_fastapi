from fastapi import FastAPI
from database import engine, Base
from decouple import config
from products.routers import router as router_product

from users.routers import router as router_user


def create_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop")

@app.on_event("startup")
def on_startup():
    create_db()


JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


app.include_router(router=router_product)
app.include_router(router=router_user)

# import secrets
# secrets.token_hex(20)