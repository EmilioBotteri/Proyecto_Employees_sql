
import sqlite3

# Crear la conexión a la base de datos (si no existe, se crea)
conn = sqlite3.connect("employees.db")
cursor = conn.cursor() # Un cursor es un objeto que permite ejecutar consultas SQL

# Crear la tabla ( cada linea es una columna, el id se autoincrementa solo, y name y position no pueden ser nulos)
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   
    name TEXT NOT NULL,
    position TEXT NOT NULL
)
""")

conn.commit() # Guardar los cambios y se crea la tabla
conn.close() # Cerrar la conexión a la base de datos para liberar recursos (cerrarla siempre despues de usarla)

# Funciones Auxiliares:

def get_db_connection():
    """
    Crea y retorna una conexión a la base de datos SQLite.
    Retorna:
    conn: Objeto de conexión a la base de datos.
    """
    conn = sqlite3.connect('employees.db')
    conn.row_factory = sqlite3.Row  # permite acceder a columnas por nombre
    return conn


def search_employee_by_id(id):
    """
    Busca un empleado por su ID en la base de datos.
    Parámetros:
    id (int): ID del empleado a buscar.
    Retorna:
    tupla: (empleado dict o None, mensaje_error o None, código_estado HTTP)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (id,))
    emp = cursor.fetchone()
    conn.close()
    
    if emp:
        return dict(emp), None, 200
    else:
        return None, "Employee not found.", 404

def validate_employee_data(data, switch=True):
    """
    # Valida los datos del empleado para las operaciones POST y PATCH.
    Parámetros:
    data (dict): Datos del empleado a validar.
    switch (bool): True para POST (todos los campos requeridos), False para PATCH (campos opcionales).
    Retorna:
    tupla: (True/False, mensaje_error(si hay), código_estado HTTP)
    """
    valid_keys = {'name', 'position'}
    if not data:
        return False, "No data provided.", 400
    elif not isinstance(data, dict):
        return False, "Data must be a JSON object.", 400
    elif len(set(data.keys())) > len(valid_keys):
        return False, "Too many keys provided.", 400
    
    if switch: # Para POST
        if len(set(data.keys())) < len(valid_keys):
            return False, "Missing required keys.", 400
        elif set(data.keys()) != valid_keys:
            return False, "Invalid keys provided.", 400
        
    else: # Para PATCH
        if not set(data.keys()).issubset(valid_keys):
            return False, "Invalid keys provided.", 400
    return True, None, 200
