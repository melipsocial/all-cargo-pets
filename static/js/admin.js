let allLeads = [];

document.addEventListener("DOMContentLoaded", loadLeads);

async function loadLeads() {
    try {
        const response = await fetch('/api/admin/');
        const leads = await response.json();
        allLeads = leads;
        
        const tbody = document.getElementById('leads-body');
        tbody.innerHTML = '';
        
        if(leads.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No hay solicitudes aún.</td></tr>';
            return;
        }

        leads.forEach(lead => {
            const row = document.createElement('tr');
            let fechaReg = new Date(lead.fecha_registro).toLocaleDateString();
            let urgBadge = lead.urgencia === 'alta' ? `<span class="badge bg-alta">Alta</span>` : `<span class="badge bg-normal">Normal</span>`;
            
            let estadoSelect = `
                <select onchange="updateEstado(${lead.id}, this.value)" style="padding:0.3rem; border-radius:4px; border:1px solid #ddd">
                    <option value="nuevo" ${lead.estado_lead==='nuevo'?'selected':''}>Nuevo</option>
                    <option value="pre-calificado" ${lead.estado_lead==='pre-calificado'?'selected':''}>Pre-Calificado</option>
                    <option value="contactado" ${lead.estado_lead==='contactado'?'selected':''}>Contactado</option>
                    <option value="cerrado" ${lead.estado_lead==='cerrado'?'selected':''}>Cerrado</option>
                </select>
            `;
            
            let waLink = `https://wa.me/${(lead.whatsapp || '').replace(/\D/g,'')}`;

            row.innerHTML = `
                <td><b>#${lead.id}</b><br><small style="color:#888">${fechaReg}</small></td>
                <td>
                    <b>${lead.nombre_completo}</b><br>
                    <a href="${waLink}" target="_blank" style="text-decoration:none; color:#25D366; font-size:0.9rem;">💬 WhatsApp</a>
                </td>
                <td>
                    ${lead.pais_origen} ➔ ${lead.pais_destino}<br>
                    <small><b>Mascota:</b> ${lead.tipo_mascota}</small>
                </td>
                <td>${urgBadge}</td>
                <td>${estadoSelect}</td>
                <td>
                    <button class="btn-primary" style="padding:0.4rem 0.8rem; font-size:0.8rem;" onclick="openModal(${lead.id})">Ver Detalles Completos</button>
                </td>
            `;
            tbody.appendChild(row);
        });

    } catch (e) {
        console.error("Error loading leads", e);
    }
}

async function updateEstado(id, nuevo_estado) {
    try {
        await fetch(`/api/admin/${id}/estado`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ nuevo_estado })
        });
    } catch (e) {
        alert("Error al actualizar estado");
    }
}

function openModal(id) {
    const lead = allLeads.find(l => l.id === id);
    if(!lead) return;
    
    document.getElementById('modal-name').innerText = "Solicitud #" + lead.id + " (" + lead.nombre_completo + ")";
    
    let html = `
        <div style="grid-column: 1 / -1; background: #e0e7ff; padding: 1rem; border-radius: 8px; font-weight: bold; color: var(--primary);">
            [${lead.modalidad_caso.toUpperCase()}] / SERVICIO: ${lead.tipo_servicio.toUpperCase()}
        </div>
        
        <div><h4 style="color:#666">Mascota</h4>
        <p><b>Tipo:</b> ${lead.tipo_mascota} (${lead.raza})<br>
        <b>Edad:</b> ${lead.edad}<br>
        <b>Peso:</b> ${lead.peso} Kg</p></div>
        
        <div><h4 style="color:#666">Contacto</h4>
        <p><b>Email:</b> ${lead.email}<br>
        <b>Tel:</b> ${lead.whatsapp}</p></div>
        
        <div><h4 style="color:#666">Ruta</h4>
        <p><b>Desde:</b> ${lead.pais_origen}<br>
        <b>Hasta:</b> ${lead.pais_destino}<br>
        <b>Fecha Viaje:</b> ${lead.fecha_estimada || lead.fecha_vuelo}</p></div>
        
        <div><h4 style="color:#666">Documentos</h4>
        <p>${lead.documentacion_actual || 'No especificados'}</p></div>
        
        <div style="grid-column: 1 / -1; background: #f8f9fa; padding: 1rem; border-radius: 8px;">
            <p><b>Notas del cliente (Observaciones):</b></p>
            <p>${lead.observaciones || '<i>El cliente no dejó comentarios extra.</i>'}</p>
        </div>
        
        <div style="grid-column: 1 / -1; border-left: 4px solid var(--danger); padding: 1rem;">
            <p style="color: var(--danger);"><b>Alertas del Sistema (IA):</b></p>
            <p>${lead.notas_internas || 'Sin alertas.'}</p>
        </div>
    `;
    document.getElementById('modal-details').innerHTML = html;
    document.getElementById('leadModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('leadModal').style.display = 'none';
}
