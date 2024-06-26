document.addEventListener("DOMContentLoaded", () => {
    fetch('/obtener/historial')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(historiales => {
            const lista_historial = document.getElementById('lista_historial');
            historiales.forEach(historial => {
                const fecha = new Date(historial.fecha);
                const fecha_formateada = fecha.toLocaleDateString('es-ES', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit'
                });
                const row = document.createElement("tr");
                historial_a_agregar = {fecha: fecha_formateada, nombre_campeon: historial.nombre_campeon, torneo: historial.nombre_torneo, categoria: historial.categoria, superficie: historial.superficie}
                for (let key in historial_a_agregar) {
                    const cell = document.createElement("td");
                    cell.textContent = historial_a_agregar[key];
                    row.appendChild(cell);
                }
            lista_historial.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Ocurrio un error:', error);
        });
});