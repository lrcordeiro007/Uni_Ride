from fastapi import FastAPI, HTTPException, Depends, status, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware
import os

SECRET_KEY = os.urandom(32).hex()

app = FastAPI()

templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


models.Base.metadata.create_all(bind=engine)
app.add_middleware(SessionMiddleware, secret_key = SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")

class User(BaseModel):
    name: str
    email: str

class Ride(BaseModel):
    origin: str
    destination: str
    driver_id: int

class Driver(BaseModel):
    license_number: str
    user_id: int    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", response_class= HTMLResponse )
async def start(request : Request):
   return templates.TemplateResponse("front_page.html", {"request" : request})

@app.get("/register", response_class = HTMLResponse)
async def register_page(request : Request):
    return templates.TemplateResponse("/register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class = HTMLResponse)
async def login(
    request : Request,
    db: Session = Depends(get_db),
    email: str = Form(...),
    password: str = Form (...)
):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not pwd_context.verify(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": " Invalid email or password"},
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    request.session["user_id"]= user.id
    
    response = RedirectResponse(url = "/", status_code=status.HTTP_303_SEE_OTHER)
    return response


@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    db: Session = Depends(get_db),
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Nome de usuário já existe."},
            status_code=status.HTTP_409_CONFLICT
        )
    
    hashed_password = pwd_context.hash(password)

    new_user = models.User(name = name ,email=email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = RedirectResponse(url="/",status_code=status.HTTP_303_SEE_OTHER)
    return response

if __name__ == "__main__":
  import uvicorn 
  uvicorn.run(app,
  host="0.0.0.0", port=8000,
  reload = True)
