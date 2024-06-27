from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from models import Tenista, db, Torneo, Historial_torneos

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/tp_tenistas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some_secret_key'

@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')

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
        info_tenista = {'nombre_tenista': tenista.nombre_tenista,
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
     .all()

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

@app.route('/crear-jugador', methods=['GET'])
def mostrar_formulario_jugador():
    return render_template('crear_nuevo_jugador.html')


@app.route('/crear-jugador', methods=['POST'])
def crear_jugador():
    nombre_tenista = request.form['nombre_tenista']
    nacionalidad = request.form['nacionalidad']
    puntuacion_global = request.form['puntuacion_global']
    superficie_preferida = request.form['superficie_preferida']
    altura_cm = request.form['altura_cm']
    peso_kg = request.form['peso_kg']

    if not (0 <= int(puntuacion_global) <= 100):
        flash('La puntuación global debe estar entre 0 y 100.')
        return redirect(url_for('mostrar_formulario_jugador'))

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
    flash('Nuevo jugador creado exitosamente!')
    return redirect(url_for('mostrar_formulario_jugador'))

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)