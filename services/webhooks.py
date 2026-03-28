import os
import json
import urllib.request

def enviar_a_webhook(datos_lead: dict, id_solicitud: int):
    """
    Envía los datos de un Lead captado hacia Make.com o Zapier si la variable
    de entorno WEBHOOK_URL está configurada.
    """
    webhook_url = os.getenv("WEBHOOK_URL")
    
    # Si no hay webhook configurado, simplemente no hace nada.
    if not webhook_url:
        return
        
    # Preparamos los datos sumándoles el ID de la base de datos
    payload = datos_lead.copy()
    payload["id_solicitud"] = id_solicitud
    
    # Intentamos disparar al url
    try:
        req = urllib.request.Request(
            webhook_url, 
            data=json.dumps(payload).encode("utf-8"), 
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Error al intentar enviar el Webhook - ignorado para no bloquear: {e}")
