
employees = [
    {"id": 1, "name": "Alice", "position": "Developer"},
    {"id": 2, "name": "Bob", "position": "Designer"},
    {"id": 3, "name": "Charlie", "position": "Manager"},
    {"id": 4, "name": "Emilio", "position": "Junior"}]


# Funciones Auxiliares
def search_employee_by_id(id):
    """
    # Busca un empleado por su ID en la lista de empleados.
    Parámetros:
    id (int): ID del empleado a buscar.
    Retorna:
    tupla: (empleadoo None, mensaje_error o None, código_estado HTTP)
    """
    emp = next((emp for emp in employees if emp['id'] == id), None)
    if emp:
        return emp, None, 200
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

