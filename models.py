import db
from sqlalchemy import Column, Integer, String, REAL


class GestorProductos(db.Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, unique=True)
    nombre = Column(String, nullable=False,unique=True)
    categoria = Column(String)
    precio = Column(REAL, nullable=False)
    cantidad = Column(Integer, nullable=False)

    def __init__(self, nombre, categoria, precio, cantidad):
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return "ID: {}, Nombre:{}, Categoria:{}, Precio:{}, Cantidad:{}".format(self.id, self.nombre,
                                                                                          self.categoria,
                                                                                          self.precio, self.cantidad)