from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str = ""
    category: str = Field(min_length=2, max_length=80)
    price: float = Field(gt=0)
    image_url: str = ""
    stock: int = Field(ge=0, default=0)


class ProductOut(BaseModel):
    id: int
    seller_id: int
    name: str
    description: str
    category: str
    price: float
    image_url: str
    stock: int
    is_active: bool

    model_config = {"from_attributes": True}


class CartItemInput(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, default=1)


class CheckoutOut(BaseModel):
    order_id: int
    total: float
    status: str