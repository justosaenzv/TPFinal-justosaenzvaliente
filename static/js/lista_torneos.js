document.addEventListener("DOMContentLoaded", () => {
    fetch('/obtener/torneos')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(torneos => {
            const lista_torneos = document.getElementById('lista_torneos');
            torneos.forEach(torneo => {
                const row = document.createElement("tr");
                torneo_a_agregar = {nombre: torneo.nombre_torneo, categoria: torneo.categoria, superficie: torneo.superficie, cant_jugadores: torneo.cant_jugadores}
                for (let key in torneo_a_agregar) {
                    const cell = document.createElement("td");
                    cell.textContent = torneo_a_agregar[key];
                    row.appendChild(cell);
                }
            lista_torneos.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Ocurrio un error:', error);
        });
});