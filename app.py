import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Corrección aquí: __name__ en lugar de **name**
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imagenes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO de Imagen procesada
class Imagen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    pixels = db.Column(db.String(200))  # Ej: "R:120 G:80 B:60"

    def __repr__(self):
        return f"<Imagen {self.filename} de {self.usuario}>"

# Ruta POST para agregar una nueva entrada
@app.route('/api/add-entry', methods=['POST'])
def add_entry():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Falta contenido JSON'}), 400
    try:
        imagen = Imagen(
            usuario=data['username'],
            filename=data['filename'],
            fecha=datetime.fromisoformat(data['date']),
            pixels=data['pixels']
        )
        db.session.add(imagen)
        db.session.commit()
        return jsonify({'mensaje': 'Imagen registrada con éxito'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/imagenes', methods=['GET'])
def get_imagenes():
    try:
        imagenes = Imagen.query.all()  # Obtener todas las imágenes de la base de datos
        imagenes_data = []
        
        # Convertir los registros de las imágenes en formato JSON
        for imagen in imagenes:
            imagen_data = {
                'id': imagen.id,
                'usuario': imagen.usuario,
                'filename': imagen.filename,
                'fecha': imagen.fecha.isoformat(),  # Convertir la fecha a formato ISO
                'pixels': imagen.pixels
            }
            imagenes_data.append(imagen_data)

        # Devolver los datos en formato JSON
        return jsonify(imagenes_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta principal para mostrar todas las imágenes en una tabla HTML
@app.route('/')
def index():
    imagenes = Imagen.query.all()
    return render_template('index.html', imagenes=imagenes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
