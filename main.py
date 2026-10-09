from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional, cast

from app.database import Base, engine, get_db
from app.models import UserDB, UserRegister, UserLogin, TokenResponse
from app.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

# Database tables create karna
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Auth Service",
    description="JWT-based Authentication and RBAC Service",
    version="1.1.0"
)

security = HTTPBearer()

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(
        (UserDB.username == user.username) | (UserDB.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username or Email already registered"
        )
    
    db_user = UserDB(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully", "id": db_user.id}

@app.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    stored_hash = cast(str, user.hashed_password)
    if not verify_password(credentials.password, stored_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token: missing subject"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )
    
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )
    return user
def require_admin(current_user: UserDB = Depends(get_current_user)):
    if str(current_user.role) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

@app.get("/profile")
def get_profile(current_user: UserDB = Depends(get_current_user)):
    return {
        "status": "Authorized",
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

@app.get("/admin/users")
def get_all_users(admin: UserDB = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return [
        {"id": u.id, "username": u.username, "email": u.email, "role": u.role} 
        for u in users
    ]