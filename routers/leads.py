from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import Lead
from pydantic import BaseModel, Field
from typing import Optional
from services.clasificacion import pre_calificar_lead

router = APIRouter()

# Simple schema para recibir datos (Flexible para MVP)
class LeadCreate(BaseModel):
    nombre_completo: str
    pais_origen: str
    pais_destino: str
    fecha_estimada: str
    tipo_mascota: str
    raza: str
    peso: str
    edad: str
    email: str
    whatsapp: str
    tipo_solicitud: str  # Viajar con mi mascota | Enviar / trasladar
    tipo_servicio: str   # solo asesoría | gestión completa
    aerolinea: Optional[str] = None
    fecha_vuelo: Optional[str] = None
    cabina_o_bodega: Optional[str] = None
    documentacion_actual: Optional[str] = None
    observaciones: Optional[str] = None
    acompanamiento: Optional[str] = None

@router.post("/")
def create_lead(lead_in: LeadCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Convert data back to dict to process
    data = lead_in.dict(exclude_none=True)
    
    # Pasar por el motor de pre-calificación
    datos_clasificados = pre_calificar_lead(data)
    
    # Insertar en DB
    new_lead = Lead(**datos_clasificados)
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    
    # Aquí podríamos agregar "background_tasks" para mandar a Google Sheets/Webhook/Email
    # background_tasks.add_task(enviar_a_webhook, new_lead)
    
    estado_msg = "Un asesor revisará tu caso y te contactará pronto."
    if new_lead.urgencia == "alta":
        estado_msg = "Hemore recibido tu solicitud marcada como URGENTE. Serás contactado a la brevedad."
        
    return {"message": estado_msg, "lead_id": new_lead.id, "urgencia": new_lead.urgencia}
