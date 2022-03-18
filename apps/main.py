from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from database import engine, Base
from decouple import config
from products.routers import router as router_product
from users.routers import router as router_user
from decouple import config


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


conf = ConnectionConfig(
    MAIL_USERNAME = config('MAIL_USERNAME'),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM =config("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

txt = """
Thanks for using Fastapi-mail
"""


@app.post("/email")
async def simple_send(email:list[str]) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email,  # List of recipients, as many as you can pass 
        body=txt,
        subtype="txt"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})     