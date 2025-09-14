from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import clientes

app = FastAPI(title="Gestión de Clientes")

# Templates y static
app.templates = Jinja2Templates(directory="gestion_clientes/templates")
app.mount("/static", StaticFiles(directory="gestion_clientes/static"), name="static")

# Routers
app.include_router(clientes.router)