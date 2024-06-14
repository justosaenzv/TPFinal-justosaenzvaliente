document.addEventListener("DOMContentLoaded", () => {
    fetch('/obtener/tenistas')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(tenistas => {
            const lista_tenistas = document.getElementById('lista_tenistas');
            tenistas.forEach(tenista => {
                const li = document.createElement('li');
                li.textContent = `${tenista.nombre_tenista} - Puntuación: ${tenista.puntuacion_global}, Superficie Preferida: ${tenista.superficie_preferida}, Nacionalidad: ${tenista.nacionalidad}, Altura: ${tenista.altura_cm} cm, Peso: ${tenista.peso_kg} kg`;
                lista_tenistas.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Ocurrio un error:', error);
        });
});

document.getElementById('submitBtn').addEventListener('click', function() {
    var nombre_tenista = document.getElementById('tenistaInput').value;
    fetch('/obtener/tenista', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre: nombre_tenista }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            window.location.href = `/tenistas/${data.id}`;
        } else {
            alert('No se encontro el tenista que buscabas, fijate de no tener faltas de ortografia y de no ser asi puedes agregar tu tenista a nuestra lista.');
        }
    });
});