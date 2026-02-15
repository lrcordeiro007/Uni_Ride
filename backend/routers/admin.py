import os
from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal

router = APIRouter(prefix="/admin", tags=["Administração"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "frontend"))
templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@router.post("/login")
async def admin_login_process(request: Request, admin_key: str = Form(...)):
    if admin_key == os.getenv("ADMIN_SECRET"):
        request.session["is_admin"] = True
        return RedirectResponse(url="/admin/users", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Chave Inválida"})


@router.get("/users", response_class=HTMLResponse)
async def admin_users_page(request: Request, search: str = None, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)

    query = db.query(models.User)
    if search:
        query = query.filter(models.User.name.ilike(f"%{search}%"))
    
    users = query.all()
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": users, "search": search})

@router.get("/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_page(request: Request, user_id: int, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/admin/login")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("admin_edit_user.html", {"request": request, "user": user})

@router.post("/update/{user_id}")
async def update_user(user_id: int, request: Request, name: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/admin/login")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.name = name
        user.email = email
        db.commit()
    return RedirectResponse(url="/admin/users", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/delete/{user_id}")
async def admin_delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/admin/login")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return RedirectResponse(url="/admin/users", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/logout")
async def admin_logout(request: Request):
    request.session.pop("is_admin", None)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)