from database import Database

class Empleado:
    """Clase para gestionar empleados"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def crear(self, nombre: str, cargo: str):
        """Crea un nuevo empleado"""
        query = "INSERT INTO Empleado (Nombre, Cargo) VALUES (?, ?)"
        empleado_id = self.db.execute_query(query, (nombre, cargo))
        print(f"[v0] Empleado creado con ID: {empleado_id}")
        return empleado_id
    
    def obtener(self, id_empleado: int):
        """Obtiene un empleado por ID"""
        query = "SELECT * FROM Empleado WHERE ID_Empleado = ?"
        return self.db.fetch_one(query, (id_empleado,))
    
    def listar(self):
        """Lista todos los empleados"""
        query = "SELECT * FROM Empleado"
        return self.db.fetch_all(query)
    
    def actualizar(self, id_empleado: int, nombre: str, cargo: str):
        """Actualiza un empleado"""
        query = "UPDATE Empleado SET Nombre = ?, Cargo = ? WHERE ID_Empleado = ?"
        self.db.execute_query(query, (nombre, cargo, id_empleado))
        print(f"[v0] Empleado {id_empleado} actualizado")
    
    def eliminar(self, id_empleado: int):
        """Elimina un empleado"""
        query = "DELETE FROM Empleado WHERE ID_Empleado = ?"
        self.db.execute_query(query, (id_empleado,))
        print(f"[v0] Empleado {id_empleado} eliminado")
