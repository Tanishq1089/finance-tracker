from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from ..database import get_db
from ..models.user import User
from ..utils.jwt_handler import create_access_token, verify_token
from ..utils.otp_handler import generate_otp, verify_otp
from ..utils.email_handler import send_otp_email

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str

class OTPRequest(BaseModel):
    email: str

class OTPVerify(BaseModel):
    email: str
    otp: str

class LoginRequest(BaseModel):
    email: str
    password: str

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/send-otp")
def send_otp(data: OTPRequest, db: Session = Depends(get_db)):
    # works for both register (new user) and login (existing user)
    otp = generate_otp(data.email)
    try:
        send_otp_email(data.email, otp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email send failed: {str(e)}")
    return {"msg": "OTP sent to your email"}

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed = pwd_context.hash(data.password)
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hashed
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"msg": "User created", "id": user.id}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify-otp")
def verify_otp_and_login(data: OTPVerify, db: Session = Depends(get_db)):
    if not verify_otp(data.email, data.otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "username": user.username}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}