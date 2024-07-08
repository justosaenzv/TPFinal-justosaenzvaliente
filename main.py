from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from models import Tenista, db, Torneo, Historial_torneos
from datetime import datetime
import random

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/tp_tenistas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/', methods=['GET'])
def pagina_inicio():
    return render_template('index.html')


@app.route('/tenistas/')
def mostrar_tenistas():
    return render_template('lista_tenistas.html')


@app.route('/torneos/')
def mostrar_torneos():
    return render_template('lista_torneos.html')


@app.route('/historial/')
def mostrar_historial():
    return render_template('lista_historial.html')


@app.route('/tenistas/<id>')
def mostrar_tenista(id):
    tenista = Tenista.query.get(id)
    if tenista:
        cantidad_torneos_ganados = Historial_torneos.query.filter_by(id_ganador=tenista.id).count()
        info_tenista = {
        'nombre_tenista': tenista.nombre_tenista,
        'puntuacion_global': tenista.puntuacion_global,
        'superficie_preferida': tenista.superficie_preferida,
        'nacionalidad': tenista.nacionalidad,
        'altura_cm': tenista.altura_cm,
        'peso_kg': tenista.peso_kg,
        'cant_torneos_ganados': cantidad_torneos_ganados
        }
        return render_template('mostrar_tenista.html', tenista=info_tenista)
    else:
        return jsonify({'error': 'Tenista no encontrado'}), 404


@app.route('/obtener/tenistas', methods=['GET'])
def obtener_info_tenistas():
    tenistas = Tenista.query.all()
    lista_tenistas = [{
        'nombre_tenista': t.nombre_tenista,
        'puntuacion_global': t.puntuacion_global,
        'superficie_preferida': t.superficie_preferida,
        'nacionalidad': t.nacionalidad,
        'altura_cm': t.altura_cm,
        'peso_kg': t.peso_kg
    } for t in tenistas]
    return jsonify(lista_tenistas)


@app.route('/obtener/torneos', methods=['GET'])
def obtener_info_torneos():
    torneos = Torneo.query.all()
    lista_torneos = [{
        'nombre_torneo': t.nombre_torneo,
        'categoria': t.categoria,
        'superficie': t.superficie,
        'cant_jugadores': t.cant_jugadores
    } for t in torneos]
    return jsonify(lista_torneos)


@app.route('/obtener/historial', methods=['GET'])
def obtener_historial():
    historial = db.session.query(
        Historial_torneos.fecha,
        Tenista.nombre_tenista,
        Torneo.nombre_torneo,
        Torneo.categoria,
        Torneo.superficie
    ).join(Tenista, Historial_torneos.id_ganador == Tenista.id)\
     .join(Torneo, Historial_torneos.torneo_id == Torneo.id)\
     .order_by(Historial_torneos.fecha.desc()).all()

    lista_historial = [{
        'fecha': h.fecha,
        'nombre_campeon': h.nombre_tenista,
        'nombre_torneo': h.nombre_torneo,
        'categoria': h.categoria,
        'superficie': h.superficie
    } for h in historial]

    return jsonify(lista_historial)

@app.route('/obtener/idtenista', methods=['POST'])
def obtener_tenista_por_nombre():
    data = request.get_json()
    nombre = data.get('nombre')
    tenista = Tenista.query.filter_by(nombre_tenista=nombre).first()
    if tenista:
        return jsonify({'id': tenista.id})
    else:
        return jsonify({'error': 'Tenista no encontrado'}), 404


@app.route('/crear-jugador', methods=['GET', 'POST'])
def crear_jugador():
    if request.method == 'POST':
        nombre_tenista = request.form['nombre_tenista']
        nacionalidad = request.form['nacionalidad']
        puntuacion_global = request.form['puntuacion_global']
        superficie_preferida = request.form['superficie_preferida']
        altura_cm = request.form['altura_cm']
        peso_kg = request.form['peso_kg']

        nuevo_tenista = Tenista(
            nombre_tenista=nombre_tenista,
            nacionalidad=nacionalidad,
            puntuacion_global=puntuacion_global,
            superficie_preferida=superficie_preferida,
            altura_cm=altura_cm,
            peso_kg=peso_kg
        )

        db.session.add(nuevo_tenista)
        db.session.commit()
        
        return render_template('crear_jugador.html', success=True)
    
    return render_template('crear_jugador.html')


@app.route('/crear-torneo', methods=['GET', 'POST'])
def crear_torneo():
    if request.method == 'POST':
        nombre_torneo = request.form['nombre_torneo']
        categoria = request.form['categoria']
        superficie = request.form['superficie']
        
        nuevo_torneo = Torneo(
            nombre_torneo=nombre_torneo,
            categoria=categoria,
            superficie=superficie
        )
        db.session.add(nuevo_torneo)
        db.session.commit()
        
        return render_template('crear_torneo.html', success=True)
    
    return render_template('crear_torneo.html', success=False)


@app.route('/crear-historial-torneo', methods=['GET', 'POST'])
def crear_historial_torneo():
    if request.method == 'POST':
        fecha = request.form['fecha']
        torneo_id = request.form['torneo']
        id_ganador = request.form['jugador_ganador']
        
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()

        nuevo_registro = Historial_torneos(
            fecha=fecha,
            torneo_id=torneo_id,
            id_ganador=id_ganador
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        
        return render_template('crear_historial.html', success=True, torneos=Torneo.query.all(), jugadores=Tenista.query.all())
    
    return render_template('crear_historial.html', torneos=Torneo.query.all(), jugadores=Tenista.query.all())


@app.route('/simular-torneo', methods=['GET', 'POST'])
def seleccionar_torneo():
    if request.method == 'POST':
        torneo_id = request.form['torneo']
        return redirect(url_for('seleccionar_jugadores', torneo_id=int(torneo_id)))

    torneos = Torneo.query.all()
    return render_template('seleccionar_torneo.html', torneos=torneos)


@app.route('/seleccionar-jugadores/<int:torneo_id>/', methods=['GET', 'POST'])
def seleccionar_jugadores(torneo_id):
    torneo = Torneo.query.get(torneo_id)
    jugadores = Tenista.query.all()
    if request.method == 'POST':
        jugadores_ids = request.form.getlist('jugadores_ids')
        if len(jugadores_ids) != torneo.cant_jugadores:
            return render_template('seleccionar_jugadores.html', torneo=torneo, jugadores=jugadores, error_cant_ids=True)
        else:
            return redirect(url_for('mostrar_campeon', torneo_id=torneo_id, jugadores_ids=','.join(jugadores_ids)))

    return render_template('seleccionar_jugadores.html', torneo=torneo, jugadores=jugadores)


@app.route('/agregar-historial/', methods=['POST'])
def agregar_historial():
    torneo_id = request.form['torneo_id']
    id_ganador = request.form['id_ganador']
    fecha = datetime.now().date()

    nuevo_historial = Historial_torneos(
        torneo_id=torneo_id,
        id_ganador=id_ganador,
        fecha=fecha
    )
    db.session.add(nuevo_historial)
    db.session.commit()

    return render_template('index.html', historial_agregado=True)


@app.route('/campeon/<int:torneo_id>/<jugadores_ids>')
def mostrar_campeon(torneo_id,jugadores_ids):

    torneo = Torneo.query.get(torneo_id)
    jugadores_ids = jugadores_ids.split(',')
    lista_jugadores = []
    for id_jugador in jugadores_ids:
        jugador = Tenista.query.get(int(id_jugador))
        lista_jugadores.append(jugador)
        
    puntuaciones = []
    for jugador in lista_jugadores:
        puntuacion = random.random() * jugador.puntuacion_global
        if jugador.superficie_preferida == torneo.superficie:
            puntuacion *= 1.20
        puntuaciones.append((jugador, puntuacion))

    ganador = max(puntuaciones, key=lambda x: x[1])[0]
    
    return render_template('mostrar_campeon.html', ganador=ganador, torneo=torneo)


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)