from flask import Flask, jsonify, render_template, request
from models import Tenista, db

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/tp_tenistas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/obtener/tenistas', methods=['GET'])
def obtener_info_tenistas():
    tenistas = Tenista.query.all()
    tenistas_list = [{
        'id': t.id,
        'nombre_tenista': t.nombre_tenista,
        'puntuacion_global': t.puntuacion_global,
        'superficie_preferida': t.superficie_preferida,
        'nacionalidad': t.nacionalidad,
        'altura_cm': t.altura_cm,
        'peso_kg': t.peso_kg
    } for t in tenistas]
    return jsonify(tenistas_list)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')

@app.route('/obtener/tenista', methods=['POST'])  
def obtener_tenista_por_nombre():
    data = request.get_json()
    nombre = data.get('nombre')
    tenista = Tenista.query.filter_by(nombre_tenista=nombre).first()
    if tenista:
        return jsonify({'id': tenista.id})
    else:
        return jsonify({'error': 'Tenista no encontrado'}), 404

@app.route('/tenistas/<id>')
def mostrar_tenista(id):
    tenista = Tenista.query.get(id)
    if tenista:
        return render_template('mostrar_tenista.html', tenista=tenista)
    else:
        return jsonify({'error': 'Tenista no encontrado'}), 404



if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)