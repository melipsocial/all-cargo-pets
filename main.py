from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
import routers.leads as leads_router
import routers.admin as admin_router
import os

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="All Cargo Pets API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Register Routers
app.include_router(leads_router.router, prefix="/api/leads", tags=["leads"])
app.include_router(admin_router.router, prefix="/api/admin", tags=["admin"])

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/solicitud")
def form_solicitud(request: Request):
    return templates.TemplateResponse("solicitud.html", {"request": request})

@app.get("/dashboard")
def get_dashboard(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
