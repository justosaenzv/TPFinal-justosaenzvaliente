from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tenista(db.Model):
    __tablename__ = 'tenistas'

    id = db.Column(db.Integer, primary_key=True)
    nombre_tenista = db.Column(db.String)
    puntuacion_global = db.Column(db.Integer, db.CheckConstraint('puntuacion_global >= 0 AND puntuacion_global <= 100'))
    superficie_preferida = db.Column(db.Enum('Polvo de ladrillo', 'Cemento', 'Pasto', name='superficie_valida'))
    nacionalidad = db.Column(db.String)
    altura_cm = db.Column(db.Integer)
    peso_kg = db.Column(db.Integer)


class Torneo(db.Model):
    __tablename__ = 'torneos'

    id = db.Column(db.Integer, primary_key=True)
    nombre_torneo = db.Column(db.String)
    categoria = db.Column(db.Enum('Grand Slam', 'Master 1000', 'ATP 500', 'ATP 250', name='categoria_valida'))
    superficie = db.Column(db.Enum('Polvo de ladrillo', 'Cemento', 'Pasto', name='superficie_valida'))
    cant_jugadores = db.Column(db.Integer)

    @property
    def cant_jugadores(self):
        if self.categoria == 'Grand Slam':
            return 16
        elif self.categoria == 'Master 1000':
            return 8
        elif self.categoria == 'ATP 500':
            return 4
        elif self.categoria == 'ATP 250':
            return 2
        else:
            return 0


class Historial_torneos(db.Model):
    __tablename__ = 'historial_torneos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    torneo_id = db.Column(db.Integer, db.ForeignKey('torneos.id'), nullable=False)
    id_ganador = db.Column(db.Integer, db.ForeignKey('tenistas.id'), nullable=False)