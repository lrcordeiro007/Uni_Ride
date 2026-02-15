import os
import shutil
from fastapi import APIRouter, Depends, Request, Form, File, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal

router = APIRouter(prefix="/profile", tags=["Perfil"])

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Como este arquivo está dentro de /routers, precisamos subir dois níveis para achar /frontend
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "frontend"))
UPLOAD_DIR = os.path.join(FRONTEND_DIR, "static", "uploads")
templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))

# Dependência do Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS ---

@router.get("/", response_class=HTMLResponse)
async def profile_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@router.post("/update")
async def update_profile(
    request: Request, 
    name: str = Form(...),
    profile_file: UploadFile = File(None),
    car_model: str = Form(None),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user:
        user.name = name
        
        # Lógica de Upload de Arquivo
        if profile_file and profile_file.filename:
            # Garante que a pasta de upload existe
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            
            ext = os.path.splitext(profile_file.filename)[1]
            filename = f"user_avatar_{user.id}{ext}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(profile_file.file, buffer)
            
            # Atualiza o caminho da imagem no banco
            user.profile_pic = f"/static/uploads/{filename}"
            
        # Atualização do modelo do carro (apenas se for motorista)
        if user.driver_profile and car_model:
            user.driver_profile.license_number = car_model
            
        db.commit()
    
    return RedirectResponse(url="/profile", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/become-driver")
async def become_driver(
    request: Request, 
    license_number: str = Form(...), 
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user and not user.driver_profile:
        new_driver = models.Driver(
            license_number=license_number,
            user_id=user.id
        )
        db.add(new_driver)
        db.commit()
    
    return RedirectResponse(url="/profile", status_code=303)