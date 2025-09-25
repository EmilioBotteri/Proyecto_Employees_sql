
from flask import Blueprint, request, jsonify
from services.service import search_employee_by_id, validate_employee_data, employees

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/')
def home():
    """
    # Página de inicio de la API.
    Retorna:
    Mensaje de bienvenida.
    """
    return "Welcome to the Employee API"

@employees_bp.route('/employees', methods=['GET'])
def get_employees():
    """
    # Obtiene la lista de todos los empleados.
    Retorna:
    Lista de empleados en formato JSON.
    """
    return jsonify(employees)

@employees_bp.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    """
    # Obtiene un empleado por su ID.
    Parámetros:
    id (int): ID del empleado a buscar.
    Retorna:
    Empleado en formato JSON o mensaje de error, mas codigo de estado HTTP.
    """
    emp, error, status_code = search_employee_by_id(id)
    if emp is None:
        return jsonify({"error": error}), status_code
    return jsonify(emp), 200

@employees_bp.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    """
    # Elimina un empleado por su ID.
    Parámetros:
    id (int): ID del empleado a eliminar.
    Retorna:
    Mensaje de confirmación o error, mas codigo de estado HTTP.
    """
    emp, error, status_code = search_employee_by_id(id)
    if emp is None:
        return jsonify({"error": error}), status_code
    employees.remove(emp)
    return jsonify({"message": f"Employee with id {id} deleted."}), 200

@employees_bp.route('/employees', methods=['POST'])
def add_employee():
    """
    # Agrega un nuevo empleado.
    Parametros implicitos:
    JSON en el cuerpo de la request con las claves obligatorias:
        - name (str): Nombre del empleado.
        - position (str): Puesto del empleado.
    Retorna:
    Empleado creado en formato JSON o mensaje de error, mas codigo de estado HTTP.
    """
    new_emp = request.get_json()
    check, error, status_code = validate_employee_data(new_emp, switch=True)
    if check is False:
        return jsonify({"error": error}), status_code
    new_id = max(emp['id'] for emp in employees) + 1 if employees else 1
    new_emp['id'] = new_id
    employees.append(new_emp)
    return jsonify(new_emp), 201

@employees_bp.route('/employees/<int:id>', methods=['PATCH'])
def update_employee(id):
    """
    # Actualiza un empleado existente.
    Parámetros:
    id (int): ID del empleado a actualizar.
    Parametros implicitos:
    JSON en el cuerpo de la request con las claves opcionales:
        - name (str): Nombre del empleado.
        - position (str): Puesto del empleado.
    Retorna:
    Empleado actualizado en formato JSON o mensaje de error, mas codigo de estado HTTP.
    """
    emp, error, status_code = search_employee_by_id(id)
    if not emp:
        return jsonify({"error": "Employee not found."}), 404
    updates = request.get_json()
    check, error, status_code = validate_employee_data(updates, switch=False)
    if check is False:
        return jsonify({"error": error}), status_code
    emp.update(updates)
    return jsonify(emp), 200
