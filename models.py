from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
import datetime

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow)
    nombre_completo = Column(String, index=True)
    pais_origen = Column(String)
    pais_destino = Column(String)
    fecha_estimada = Column(String)  # We keep as string to accept "2024-05-12"
    tipo_mascota = Column(String)
    raza = Column(String)
    peso = Column(String)
    edad = Column(String)
    email = Column(String, index=True)
    whatsapp = Column(String)
    tipo_solicitud = Column(String)  # 'Viajar con mascota' or 'Trasladar mascota'
    tipo_servicio = Column(String)   # 'solo asesoría' or 'gestión completa'
    
    # Específicos Viaje
    aerolinea = Column(String, nullable=True)
    fecha_vuelo = Column(String, nullable=True)
    cabina_o_bodega = Column(String, nullable=True)
    
    # Específicos Traslado
    acompanamiento = Column(String, nullable=True)
    
    # Comunes a ambos o extra
    documentacion_actual = Column(String, nullable=True)
    observaciones = Column(Text, nullable=True)

    # Campos calculados / automáticos
    modalidad_caso = Column(String) # viaje_con_mascota | traslado_internacional
    urgencia = Column(String)       # alta | media | normal
    estado_lead = Column(String, default="nuevo") # nuevo | pre-calificado | contactado | en proceso | cerrado
    tags = Column(String)   # Comma separated tags
    notas_internas = Column(Text, nullable=True)
