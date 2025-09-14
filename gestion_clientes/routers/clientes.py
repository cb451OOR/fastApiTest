from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter()

# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Rutas HTML ----------------

# Lista de clientes
@router.get("/", name="lista_clientes")
def lista_clientes(request: Request, db: Session = Depends(get_db)):
    clientes = db.query(models.Client).all()
    return request.app.templates.TemplateResponse("clientes/lista.html", {"request": request, "clientes": clientes})

# Formulario nuevo cliente
@router.get("/nuevo", name="nuevo_cliente")
def nuevo_cliente(request: Request):
    return request.app.templates.TemplateResponse("clientes/editar.html", {"request": request, "cliente": None})

# Crear cliente
@router.post("/nuevo")
def crear_cliente(nombre: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    cliente = models.Client(name=nombre, email=email)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)

# Editar cliente - GET
@router.get("/editar/{cliente_id}", name="editar_cliente")
def editar_cliente(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Client).filter(models.Client.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return request.app.templates.TemplateResponse("clientes/editar.html", {"request": request, "cliente": cliente})

# Editar cliente - POST
@router.post("/editar/{cliente_id}")
def editar_cliente_post(cliente_id: int, nombre: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    cliente = db.query(models.Client).filter(models.Client.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente.name = nombre
    cliente.email = email
    db.commit()
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)

# Confirmar eliminación
@router.get("/eliminar/{cliente_id}", name="confirmar_eliminar_cliente")
def confirmar_eliminar_cliente(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Client).filter(models.Client.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return request.app.templates.TemplateResponse("clientes/confirmar_eliminar.html", {"request": request, "cliente": cliente})

# Eliminar cliente
@router.post("/eliminar/{cliente_id}", name="eliminar_cliente")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Client).filter(models.Client.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(cliente)
    db.commit()
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
