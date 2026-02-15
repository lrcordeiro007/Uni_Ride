import os
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from authlib.integrations.starlette_client import OAuth

import models
from database import SessionLocal

router = APIRouter(tags=["Autenticação"])

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def auth_google(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        return RedirectResponse(url="/login?error=falha_na_autenticacao", status_code=303)
    
    user_info = token.get('userinfo')
    email = user_info.get('email')
    google_id = user_info.get('sub')
    picture_url = user_info.get('picture')

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        user = models.User(
            name=user_info.get('name', 'Usuário Google'),
            email=email,
            google_id=google_id,
            profile_pic=picture_url
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if not user.google_id:
            user.google_id = google_id
        user.profile_pic = picture_url
        db.commit()

    request.session["user_id"] = user.id
    return RedirectResponse(url="/ride", status_code=303)

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user or not user.hashed_password:
        return RedirectResponse(url="/login?error=use_google", status_code=303)
    
    if not pwd_context.verify(password[:72], user.hashed_password):
        return RedirectResponse(url="/login?error=senha_incorreta", status_code=303)
    
    request.session["user_id"] = user.id
    return RedirectResponse(url="/ride", status_code=303)

@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db), name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return RedirectResponse(url="/register?error=email_existe", status_code=303)
    
    new_user = models.User(
        name=name, 
        email=email, 
        hashed_password=pwd_context.hash(password[:72])
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)