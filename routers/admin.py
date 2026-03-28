from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Lead
from pydantic import BaseModel

router = APIRouter()

class UpdateEstado(BaseModel):
    nuevo_estado: str

@router.get("/")
def get_all_leads(db: Session = Depends(get_db)):
    # Para producción, se debe añadir paginación y filtros reales.
    # Por ahora trae todo ordenado por fecha descendente.
    return db.query(Lead).order_by(Lead.id.desc()).all()

@router.put("/{lead_id}/estado")
def update_lead_state(lead_id: int, payload: UpdateEstado, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead.estado_lead = payload.nuevo_estado
    db.commit()
    db.refresh(lead)
    return {"status": "ok", "nuevo_estado": lead.estado_lead}
