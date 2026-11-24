import hashlib
import secrets
from decimal import Decimal

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import CartItem, Order, Product, User
from .schemas import (
    CartItemInput,
    CheckoutOut,
    LoginRequest,
    ProductCreate,
    ProductOut,
    TokenOut,
    UserCreate,
    UserOut,
)

app = FastAPI(title="Mera Marketplace API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4173", "http://127.0.0.1:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
TOKENS: dict[str, int] = {}


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.scrypt(password.encode(), salt=salt.encode(), n=2**14, r=8, p=1).hex()
    return f"{salt}${digest}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, digest = password_hash.split("$", 1)
        candidate = hashlib.scrypt(password.encode(), salt=salt.encode(), n=2**14, r=8, p=1).hex()
        return secrets.compare_digest(candidate, digest)
    except (ValueError, TypeError):
        return False


def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    token = authorization.removeprefix("Bearer ").strip()
    user_id = TOKENS.get(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "mera-backend"}


@app.post("/api/auth/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    if "@" not in email:
        raise HTTPException(status_code=422, detail="A valid email address is required")
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(name=payload.name.strip(), email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = secrets.token_urlsafe(32)
    TOKENS[token] = user.id
    return {"access_token": token, "token_type": "bearer", "user": user}


@app.post("/api/auth/login", response_model=TokenOut)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.strip().lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = secrets.token_urlsafe(32)
    TOKENS[token] = user.id
    return {"access_token": token, "token_type": "bearer", "user": user}


@app.get("/api/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@app.get("/api/products", response_model=list[ProductOut])
def list_products(category: str | None = Query(default=None), db: Session = Depends(get_db)):
    statement = select(Product).where(Product.is_active == True)
    if category:
        statement = statement.where(Product.category.ilike(category))
    return db.scalars(statement).all()


@app.post("/api/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = Product(seller_id=user.id, **payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get("/api/cart")
def get_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.scalars(select(CartItem).where(CartItem.user_id == user.id)).all()
    result = []
    subtotal = Decimal("0")
    for item in items:
        product = db.get(Product, item.product_id)
        if product:
            line_total = Decimal(str(product.price)) * item.quantity
            subtotal += line_total
            result.append({"id": item.id, "quantity": item.quantity, "product": ProductOut.model_validate(product).model_dump(), "line_total": float(line_total)})
    return {"items": result, "subtotal": float(subtotal)}


@app.post("/api/cart")
def add_to_cart(payload: CartItemInput, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.get(Product, payload.product_id)
    if not product or not product.is_active:
        raise HTTPException(status_code=404, detail="Product not found")
    if payload.quantity > product.stock:
        raise HTTPException(status_code=409, detail="Not enough stock")
    item = db.scalar(select(CartItem).where(CartItem.user_id == user.id, CartItem.product_id == product.id))
    if item:
        item.quantity += payload.quantity
    else:
        item = CartItem(user_id=user.id, product_id=product.id, quantity=payload.quantity)
        db.add(item)
    db.commit()
    return {"message": "Added to cart"}


@app.delete("/api/cart/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user.id))
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()


@app.post("/api/checkout", response_model=CheckoutOut)
def checkout(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.scalars(select(CartItem).where(CartItem.user_id == user.id)).all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    total = Decimal("0")
    for item in items:
        product = db.get(Product, item.product_id)
        if not product or not product.is_active:
            raise HTTPException(status_code=409, detail="A cart item is no longer available")
        if item.quantity > product.stock:
            raise HTTPException(status_code=409, detail=f"Not enough stock for {product.name}")
        total += Decimal(str(product.price)) * item.quantity
    order = Order(user_id=user.id, total=float(total), status="pending")
    db.add(order)
    for item in items:
        product = db.get(Product, item.product_id)
        product.stock -= item.quantity
        db.delete(item)
    db.commit()
    db.refresh(order)
    return {"order_id": order.id, "total": float(order.total), "status": order.status}
