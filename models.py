from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = "cliente"

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)

class Empleado(db.Model):
    __tablename__ = "empleado"

    id_empleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)

class Producto(db.Model):
    __tablename__ = "producto"

    id_producto = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)

class Renta(db.Model):
    __tablename__ = "renta"

    id_renta = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer)
    id_empleado = db.Column(db.Integer)
    id_producto = db.Column(db.Integer)

    fecha_renta = db.Column(db.Date)
    fecha_devolucion = db.Column(db.Date)

    estado_renta = db.Column(db.String)
    pago_total = db.Column(db.Float)

  #  cliente = db.relationship("Cliente")
  # empleado = db.relationship("Empleado")
  #  producto = db.relationship("Producto")
