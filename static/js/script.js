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
            console.error('There has been a problem with your fetch operation:', error);
        });
});