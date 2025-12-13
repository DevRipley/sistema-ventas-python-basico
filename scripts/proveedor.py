from database import Database

class Proveedor:
    """Clase para gestionar proveedores"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def crear(self, nombre: str, telefono: str = "", direccion: str = ""):
        """Crea un nuevo proveedor"""
        query = "INSERT INTO Proveedor (Nombre, Telefono, Direccion) VALUES (?, ?, ?)"
        proveedor_id = self.db.execute_query(query, (nombre, telefono, direccion))
        print(f"[v0] Proveedor creado con ID: {proveedor_id}")
        return proveedor_id
    
    def obtener(self, id_proveedor: int):
        """Obtiene un proveedor por ID"""
        query = "SELECT * FROM Proveedor WHERE ID_Proveedor = ?"
        return self.db.fetch_one(query, (id_proveedor,))
    
    def listar(self):
        """Lista todos los proveedores"""
        query = "SELECT * FROM Proveedor"
        return self.db.fetch_all(query)
    
    def actualizar(self, id_proveedor: int, nombre: str, telefono: str, direccion: str):
        """Actualiza un proveedor"""
        query = "UPDATE Proveedor SET Nombre = ?, Telefono = ?, Direccion = ? WHERE ID_Proveedor = ?"
        self.db.execute_query(query, (nombre, telefono, direccion, id_proveedor))
        print(f"[v0] Proveedor {id_proveedor} actualizado")
    
    def eliminar(self, id_proveedor: int):
        """Elimina un proveedor"""
        query = "DELETE FROM Proveedor WHERE ID_Proveedor = ?"
        self.db.execute_query(query, (id_proveedor,))
        print(f"[v0] Proveedor {id_proveedor} eliminado")
