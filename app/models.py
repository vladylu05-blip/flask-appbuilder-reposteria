from datetime import datetime

from flask_appbuilder import Model
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship


class Categoria(Model):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(250), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return self.nombre


class Ingrediente(Model):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    categoria = relationship("Categoria")
    cantidad = Column(Numeric(12, 3), nullable=False, default=0)
    unidad_medida = Column(String(20), nullable=False)
    costo_unitario = Column(Numeric(12, 2), nullable=False, default=0)
    stock_minimo = Column(Numeric(12, 3), nullable=False, default=0)
    fecha_vencimiento = Column(Date, nullable=True)
    activo = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return self.nombre


class Plato(Model):
    __tablename__ = "platos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), unique=True, nullable=False)
    descripcion = Column(String(250), nullable=True)
    precio = Column(Numeric(12, 2), nullable=False, default=0)
    activo = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return self.nombre


class Receta(Model):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True)
    plato_id = Column(Integer, ForeignKey("platos.id"), nullable=False)
    plato = relationship("Plato")
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), nullable=False)
    ingrediente = relationship("Ingrediente")
    cantidad_necesaria = Column(Numeric(12, 3), nullable=False)

    def __repr__(self):
        return f"{self.plato} - {self.ingrediente}"


class MovimientoInventario(Model):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), nullable=False)
    ingrediente = relationship("Ingrediente")
    # USUARIOS = tabla ab_user de Flask-AppBuilder (ya tiene id y username)
    usuario_id = Column(Integer, ForeignKey("ab_user.id"), nullable=False)
    usuario = relationship(User)
    tipo = Column(String(10), nullable=False)  # ENTRADA / SALIDA
    cantidad = Column(Numeric(12, 3), nullable=False)
    motivo = Column(String(250), nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"{self.tipo} {self.cantidad} {self.ingrediente}"
