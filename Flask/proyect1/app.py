

from flask import Flask
from routes.rutas import employees_bp  # Importamos el blueprint

app = Flask(__name__)
app.register_blueprint(employees_bp)  # Registramos las rutas

if __name__ == "__main__":
    app.run(port=8000, debug=False)

