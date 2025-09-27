
from flask import Flask
from routes.rutas_sql import employees_bp  

app = Flask(__name__)
app.register_blueprint(employees_bp)    

if __name__ == "__main__":
    app.run(port=8000, debug=False)


