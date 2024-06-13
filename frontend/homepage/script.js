document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/obtener/tenistas')
        .then(response => response.json())
        .then(data => {
            const tenistasList = document.getElementById('tenistas-list');
            data.forEach(tenista => {
                const li = document.createElement('li');
                li.textContent = `${tenista.nombre_tenista} - Puntuación: ${tenista.puntuacion_global}`;
                tenistasList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching tenistas:', error));
});
