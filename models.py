from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Tenista():
    __tablename__ = 'tenistas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    puntuacion_global = db.Column(db.Integer, db.CheckConstraint('puntuacion_global <= 100'))
