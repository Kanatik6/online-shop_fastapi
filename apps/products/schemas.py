from pydantic import BaseModel, Field

class CartProduct(BaseModel):
    amount_products: int = 0

    class Config:
        orm_mode = True


class Product(BaseModel):
    title: str = Field(..., min_length=5, max_length=20)
    descriptions: str = Field(..., min_length=10)
    price: int = Field(..., gt=0)
    amount: int = Field(..., gt=0)
    cart_products: list[CartProduct] |None = None

    class Config:
        orm_mode = True


class ReturnProduct(BaseModel):
    id: int
    title: str
    descriptions: str
    price: int
    amount: int

    class Config:
        orm_mode = True


class PatchProduct(BaseModel):
    descriptions: str | None = None
    title: str | None = None
    price: int | None = None
    amount: int | None = None

    class Config:
        orm_mode = True


class ReturnCart(BaseModel):
    total_price: int
    products: list[Product] | None = None

    class Config:
        orm_mode = True


class AddProduct(BaseModel):
    id: int
    amount: int
    
    
