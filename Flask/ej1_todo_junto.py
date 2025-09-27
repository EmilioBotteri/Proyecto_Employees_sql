from flask import Flask, request, jsonify
import json

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Alice", "position": "Developer"},
    {"id": 2, "name": "Bob", "position": "Designer"},
    {"id": 3, "name": "Charlie", "position": "Manager"},
    {"id": 4, "name": "Emilio", "position": "Junior"}]

# Pagina de inicio
@app.route('/')
def home():
    return "Welcome to the Employee API"

# Obtener todos los empleados
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

# Obtener un empleado por ID 
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    emp, error, status_code = search_employee_by_id(id)
    if emp is None:
        return jsonify({"error": error}), status_code
    return jsonify(emp), 200

# Eliminar un empleado por ID
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    global employees
    emp, error, status_code = search_employee_by_id(id)
    if emp is None:
        return jsonify({"error": error}), status_code
    employees.remove(emp)
    return jsonify({"message": f"Employee with id {id} deleted."}), 200

# Agregar un nuevo empleado
@app.route('/employees', methods=['POST'])
def add_employee():
    global employees
    new_emp = request.get_json()
    check, error, status_code = validate_employee_data(new_emp, switch=True)
    if check is False:
        return jsonify({"error": error}), status_code
    new_id = max(emp['id'] for emp in employees) + 1 if employees else 1
    new_emp['id'] = new_id
    employees.append(new_emp)
    return jsonify(new_emp), 201

# Actualizar un empleado por ID
@app.route('/employees/<int:id>', methods=['PATCH'])
def update_employee(id):
    global employees
    emp = search_employee_by_id(id)
    if not emp:
        return jsonify({"error": "Employee not found."}), 404
    updates = request.get_json()
    check, error, status_code = validate_employee_data(updates, switch=False)
    if check is False:
        return jsonify({"error": error}), status_code
    emp.update(updates)
    return jsonify(emp), 200


# Funciones Auxiliares
def search_employee_by_id(id):
    emp = next((emp for emp in employees if emp['id'] == id), None)
    if emp:
        return emp, None, 200
    return None, "Employee not found.", 404

def validate_employee_data(data, switch=True):
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


app.run(debug=False, port=8000)


