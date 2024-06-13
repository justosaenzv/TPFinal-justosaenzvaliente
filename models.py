from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Tenista():
    __tablename__ = 'tenistas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    puntuacion_global = db.Column(db.Integer, db.CheckConstraint('puntuacion_global >= 0 AND puntuacion_global <= 100'))

class Torneo(db.Model):
    __tablename__ = 'torneos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    tipo = db.Column(db.Enum('Grand Slam', 'Master 1000', 'ATP 500', 'ATP 250', name='tipo_valido'))
    cant_jugadores = db.Column(db.Integer)

    @property
    def cant_jugadores(self):
        if self.tipo == 'Grand Slam':
            return 16
        elif self.tipo == 'Master 1000':
            return 8
        elif self.tipo == 'ATP 500':
            return 4
        elif self.tipo == 'ATP 250':
            return 2
        else:
            return 0  # or raise an exception for an unknown type

    @cant_jugadores.setter
    def cant_jugadores(self, value):
        pass