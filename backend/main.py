import os
from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

# Imports internos
import models
from database import engine, SessionLocal
from routers import auth, profile, admin  # Importando seus novos módulos

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
# BASE_DIR aponta para /backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# FRONTEND_DIR aponta para /frontend (sobe um nível)
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

app = FastAPI(title="UniRide API")

# --- MIDDLEWARE DE SESSÃO ---
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SESSION_SECRET", "SUA_CHAVE_FIXA_MUITO_SEGURA_AQUI"),
    https_only=False, # Definir como True em produção com HTTPS
    same_site="lax"
)

# --- BANCO DE DADOS E MIGRAÇÕES ---
models.Base.metadata.create_all(bind=engine)

# Garante que as novas colunas existam sem precisar resetar o banco
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR;"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_pic VARCHAR;"))
        conn.execute(text("ALTER TABLE users ALTER COLUMN hashed_password DROP NOT NULL;"))
        conn.commit()
    except Exception as e:
        print(f"Aviso de migração automática: {e}")

# --- ARQUIVOS ESTÁTICOS E TEMPLATES ---
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# Também montamos o diretório de scripts se você o usar separadamente
if os.path.exists(os.path.join(FRONTEND_DIR, "script")):
    app.mount("/script", StaticFiles(directory=os.path.join(FRONTEND_DIR, "script")), name="script")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Dependência do Banco de Dados para as rotas da main
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- REGISTRO DOS ROUTERS (MODULARIZAÇÃO) ---
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(admin.router)

# --- ROTAS DE NAVEGAÇÃO RAIZ ---

@app.get("/", response_class=HTMLResponse)
async def start(request: Request):
    """Página inicial de boas-vindas."""
    return templates.TemplateResponse("front_page.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Página de registro manual."""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login (Manual e Google)."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/ride", response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    """Página principal do Mapa (Leaflet). Exige login."""
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("ride.html", {"request": request, "user": user})

# --- EXECUÇÃO ---
if __name__ == "__main__":
    import uvicorn
    # Roda o servidor. O reload=True é ótimo para o seu desenvolvimento no Ubuntu.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)