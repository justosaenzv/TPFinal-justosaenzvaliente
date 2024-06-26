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
            alert('No se encontro el jugador que buscabas. Consejo: Verifica la ortografía.');
        }
    });
});