from datetime import datetime
import re

def pre_calificar_lead(datos: dict) -> dict:
    """
    Analiza los datos del formulario (un diccionario) y agrega/modifica campos
    de modalidad, urgencia, estado y etiquetas automáticas.
    """
    tags = []
    
    # 1. Determinar modalidad general
    if datos.get("tipo_solicitud") == "Viajar con mi mascota":
        modalidad = "viaje_con_mascota"
        tags.append("viaje_internacional")
    else:
        modalidad = "traslado_internacional"
        tags.append("traslado")
        
    # Tags de mascota
    tipo_mascota = str(datos.get("tipo_mascota", "")).lower()
    if "perro" in tipo_mascota: tags.append("perro")
    if "gato" in tipo_mascota: tags.append("gato")

    # Tags de servicio
    if datos.get("tipo_servicio") == "gestión completa":
        tags.append("gestion_completa")
    else:
        tags.append("asesoria")

    # Tags específicos
    if datos.get("cabina_o_bodega") == "cabina": tags.append("cabina")
    if datos.get("cabina_o_bodega") == "bodega": tags.append("bodega")

    # 2. Motor de urgencia
    urgencia = "normal"
    notas = []
    
    # a) Checar fechas (<15 días)
    # Suponiendo formato string YYYY-MM-DD
    fecha_viaje = datos.get("fecha_vuelo") or datos.get("fecha_estimada")
    if fecha_viaje:
        try:
            fv = datetime.strptime(fecha_viaje, "%Y-%m-%d") # HTML5 date input is YYYY-MM-DD
            dias_restantes = (fv - datetime.now()).days
            if dias_restantes < 15:
                urgencia = "alta"
                notas.append(f"Urgencia por fecha: faltan {dias_restantes} días para el vuelo.")
        except:
            pass # Formato inválido o no parseable

    # b) Checar "palabras clave" en observaciones
    obs = str(datos.get("observaciones", "")).lower()
    kw_urgentes = ["urgente", "lo antes posible", "pronto", "esta semana", "próximo vuelo", "emergencia"]
    if any(kw in obs for kw in kw_urgentes):
        urgencia = "alta"
        notas.append("Palabras de urgencia detectadas en observaciones.")
        
    # c) Falta de documentos + fecha próxima
    docs = str(datos.get("documentacion_actual", "")).lower()
    if ("ninguno" in docs or "no sabe" in docs) and urgencia == "alta":
        notas.append("ALERTA CRÍTICA: Viaje urgente sin documentación previa.")
    
    # 3. Empacar y retornar el state
    datos["modalidad_caso"] = modalidad
    datos["urgencia"] = urgencia
    datos["tags"] = ",".join(tags)
    datos["estado_lead"] = "pre-calificado"
    datos["notas_internas"] = " | ".join(notas)
    
    return datos
