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
                const row = document.createElement("tr");
                tenista_a_agregar = {nombre: tenista.nombre_tenista, nacionalidad: tenista.nacionalidad, puntuacion_global: tenista.puntuacion_global, superficie_preferida: tenista.superficie_preferida, altura: tenista.altura_cm, peso: tenista.peso_kg}
                for (let key in tenista_a_agregar) {
                    const cell = document.createElement("td");
                    cell.textContent = tenista_a_agregar[key];
                    row.appendChild(cell);
                }
            lista_tenistas.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Ocurrio un error:', error);
        });
});