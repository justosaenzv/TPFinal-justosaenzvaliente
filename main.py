from flask import Flask, jsonify, send_from_directory
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
def pagina_principal():
        return send_from_directory('frontend/homepage', 'index.html')
    
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)