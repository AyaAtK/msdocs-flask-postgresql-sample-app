from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String

# Inicializa SQLAlchemy sin app
# Se llamará luego con db.init_app(app)
db = SQLAlchemy()

# Modelo para imágenes procesadas
class Imagen(db.Model):
    __tablename__ = 'imagenes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    usuario = Column(String(255), nullable=False)
    colores = Column(String, nullable=False)  # Guardamos como JSON serializado
    fecha_subida = Column(DateTime, nullable=False)
