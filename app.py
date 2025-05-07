import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, send_from_directory, url_for, jsonify
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import db, Imagen  # Cambié esto para importar el db desde models

app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # Local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # Production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Inicializamos db con app
db.init_app(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

@app.route('/', methods=['GET'])
def index():
    print('Request for index page received')
    imagenes = Imagen.query.order_by(Imagen.fecha_subida.desc()).all()
    return render_template('index.html', imagenes=imagenes)

@app.route('/upload', methods=['POST'])
@csrf.exempt
def upload_image():
    try:
        data = request.get_json()
        nombre = data['nombre']
        usuario = data['usuario']
        colores = str(data['colores'])
        fecha = datetime.now()

        imagen = Imagen(nombre=nombre, usuario=usuario, colores=colores, fecha_subida=fecha)
        db.session.add(imagen)
        db.session.commit()

        return jsonify({"mensaje": "Subida exitosa"}), 200
    except Exception as e:
        return jsonify({"mensaje": "Error al subir la imagen", "error": str(e)}), 400

@app.route('/api/imagenes', methods=['GET'])
def listar_imagenes():
    try:
        imagenes = Imagen.query.order_by(Imagen.fecha_subida.desc()).all()
        resultado = []
        for img in imagenes:
            resultado.append({
                "nombre": img.nombre,
                "usuario": img.usuario,
                "fecha": img.fecha_subida.strftime('%Y-%m-%d %H:%M:%S'),
                "colores": eval(img.colores)
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()
