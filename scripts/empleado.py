from database import Database
import hashlib

class Empleado:
    """Clase para gestionar empleados"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def _hash_password(self, password: str) -> str:
        """Hashea una contraseña usando SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def crear(self, nombre: str, cargo: str, usuario: str = None, contrasena: str = None, rol: str = 'empleado'):
        """Crea un nuevo empleado"""
        # Verificar si el usuario ya existe
        if usuario:
            existente = self.obtener_por_usuario(usuario)
            if existente:
                raise ValueError(f"El usuario '{usuario}' ya existe")
        
        if usuario and contrasena:
            contrasena_hash = self._hash_password(contrasena)
            query = "INSERT INTO Empleado (Nombre, Cargo, Usuario, Contrasena, Rol) VALUES (?, ?, ?, ?, ?)"
            empleado_id = self.db.execute_query(query, (nombre, cargo, usuario, contrasena_hash, rol))
        else:
            query = "INSERT INTO Empleado (Nombre, Cargo, Rol) VALUES (?, ?, ?)"
            empleado_id = self.db.execute_query(query, (nombre, cargo, rol))
        print(f"[v0] Empleado creado con ID: {empleado_id}")
        return empleado_id
    
    def obtener(self, id_empleado: int):
        """Obtiene un empleado por ID"""
        query = "SELECT * FROM Empleado WHERE ID_Empleado = ?"
        return self.db.fetch_one(query, (id_empleado,))
    
    def obtener_por_usuario(self, usuario: str):
        """Obtiene un empleado por nombre de usuario"""
        query = "SELECT * FROM Empleado WHERE Usuario = ?"
        return self.db.fetch_one(query, (usuario,))
    
    def autenticar(self, usuario: str, contrasena: str):
        """Autentica un empleado y retorna el empleado si las credenciales son correctas"""
        empleado = self.obtener_por_usuario(usuario)
        if empleado:
            contrasena_almacenada = empleado['Contrasena'] if 'Contrasena' in empleado.keys() else None
            if contrasena_almacenada:
                contrasena_hash = self._hash_password(contrasena)
                if contrasena_almacenada == contrasena_hash:
                    return empleado
        return None
    
    def listar(self):
        """Lista todos los empleados"""
        query = "SELECT * FROM Empleado"
        return self.db.fetch_all(query)
    
    def actualizar(self, id_empleado: int, nombre: str, cargo: str, usuario: str = None, contrasena: str = None, rol: str = None):
        """Actualiza un empleado"""
        if usuario and contrasena and rol:
            contrasena_hash = self._hash_password(contrasena)
            query = "UPDATE Empleado SET Nombre = ?, Cargo = ?, Usuario = ?, Contrasena = ?, Rol = ? WHERE ID_Empleado = ?"
            self.db.execute_query(query, (nombre, cargo, usuario, contrasena_hash, rol, id_empleado))
        elif usuario and contrasena:
            contrasena_hash = self._hash_password(contrasena)
            query = "UPDATE Empleado SET Nombre = ?, Cargo = ?, Usuario = ?, Contrasena = ? WHERE ID_Empleado = ?"
            self.db.execute_query(query, (nombre, cargo, usuario, contrasena_hash, id_empleado))
        elif usuario and rol:
            query = "UPDATE Empleado SET Nombre = ?, Cargo = ?, Usuario = ?, Rol = ? WHERE ID_Empleado = ?"
            self.db.execute_query(query, (nombre, cargo, usuario, rol, id_empleado))
        elif usuario:
            query = "UPDATE Empleado SET Nombre = ?, Cargo = ?, Usuario = ? WHERE ID_Empleado = ?"
            self.db.execute_query(query, (nombre, cargo, usuario, id_empleado))
        elif rol:
            query = "UPDATE Empleado SET Nombre = ?, Cargo = ?, Rol = ? WHERE ID_Empleado = ?"
            self.db.execute_query(query, (nombre, cargo, rol, id_empleado))
        else:
            query = "UPDATE Empleado SET Nombre = ?, Cargo = ? WHERE ID_Empleado = ?"
            self.db.execute_query(query, (nombre, cargo, id_empleado))
        print(f"[v0] Empleado {id_empleado} actualizado")
    
    def eliminar(self, id_empleado: int):
        """Elimina un empleado"""
        query = "DELETE FROM Empleado WHERE ID_Empleado = ?"
        self.db.execute_query(query, (id_empleado,))
        print(f"[v0] Empleado {id_empleado} eliminado")
