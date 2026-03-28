let currentStep = 1;
const totalSteps = 3;

function selectRadioCard(labelElement) {
    const parent = labelElement.parentElement;
    parent.querySelectorAll('.radio-card').forEach(card => card.classList.remove('selected'));
    labelElement.classList.add('selected');
}

document.getElementById('btn-next').addEventListener('click', () => {
    // Basic Validation before moving
    const formPart = document.getElementById(`card-${currentStep}`);
    const requiredInputs = formPart.querySelectorAll('input[required]');
    let valid = true;
    for(let input of requiredInputs) {
        if(!input.value) { valid = false; input.style.borderColor = 'red'; }
        else { input.style.borderColor = '#e0e0e0'; }
    }
    if(!valid) return alert("Por favor, llena los campos requeridos (*)");

    if (currentStep < totalSteps) {
        // Handle dynamic fields in Step 3 based on Step 1
        if (currentStep === 2) {
            const isViaje = document.querySelector('input[name="tipo_solicitud"]:checked').value.includes("Viajar");
            document.getElementById('dynamic-viaje').style.display = isViaje ? 'block' : 'none';
            document.getElementById('dynamic-traslado').style.display = !isViaje ? 'block' : 'none';
        }

        document.getElementById(`card-${currentStep}`).classList.remove('active');
        document.getElementById(`step-id-${currentStep}`).classList.remove('active');
        document.getElementById(`step-id-${currentStep}`).classList.add('completed');
        
        currentStep++;
        
        document.getElementById(`card-${currentStep}`).classList.add('active');
        document.getElementById(`step-id-${currentStep}`).classList.add('active');
        
        document.getElementById('btn-prev').style.visibility = 'visible';
        
        if (currentStep === totalSteps) {
            document.getElementById('btn-next').innerText = 'Enviar Solicitud ✔️';
        }
    } else if (currentStep === totalSteps) {
        submitForm();
    }
});

document.getElementById('btn-prev').addEventListener('click', () => {
    if (currentStep > 1) {
        document.getElementById(`card-${currentStep}`).classList.remove('active');
        document.getElementById(`step-id-${currentStep}`).classList.remove('active');
        
        currentStep--;
        
        document.getElementById(`card-${currentStep}`).classList.add('active');
        document.getElementById(`step-id-${currentStep}`).classList.remove('completed');
        document.getElementById(`step-id-${currentStep}`).classList.add('active');
        
        document.getElementById('btn-next').innerText = 'Siguiente paso ➔';
        if (currentStep === 1) {
            document.getElementById('btn-prev').style.visibility = 'hidden';
        }
    }
});

async function submitForm() {
    const form = document.getElementById('leadForm');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    document.getElementById('btn-next').innerText = 'Enviando...';
    document.getElementById('btn-next').disabled = true;

    try {
        const response = await fetch('/api/leads/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        
        // Show Success Step
        document.getElementById(`card-${currentStep}`).classList.remove('active');
        document.getElementById(`step-id-4`).classList.add('completed');
        document.getElementById('wizard-footer').style.display = 'none';
        
        const card4 = document.getElementById(`card-4`);
        card4.classList.add('active');
        if (result.urgencia === 'alta') {
            document.getElementById('success-message').innerText = result.message;
            document.getElementById('success-message').style.fontWeight = 'bold';
            document.getElementById('success-message').style.color = '#e63946';
        }

    } catch (err) {
        console.error(err);
        alert("Ocurrió un error al enviar tu solicitud. Intenta de nuevo.");
        document.getElementById('btn-next').innerText = 'Enviar Solicitud ✔️';
        document.getElementById('btn-next').disabled = false;
    }
}
