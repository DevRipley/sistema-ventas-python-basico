from database import Database

class Cliente:
    """Clase para gestionar clientes"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def crear(self, nombre: str, telefono: str = "", direccion: str = ""):
        """Crea un nuevo cliente"""
        query = "INSERT INTO Cliente (Nombre, Telefono, Direccion) VALUES (?, ?, ?)"
        cliente_id = self.db.execute_query(query, (nombre, telefono, direccion))
        print(f"[v0] Cliente creado con ID: {cliente_id}")
        return cliente_id
    
    def obtener(self, id_cliente: int):
        """Obtiene un cliente por ID"""
        query = "SELECT * FROM Cliente WHERE ID_Cliente = ?"
        return self.db.fetch_one(query, (id_cliente,))
    
    def listar(self):
        """Lista todos los clientes"""
        query = "SELECT * FROM Cliente"
        return self.db.fetch_all(query)
    
    def actualizar(self, id_cliente: int, nombre: str, telefono: str, direccion: str):
        """Actualiza un cliente"""
        query = "UPDATE Cliente SET Nombre = ?, Telefono = ?, Direccion = ? WHERE ID_Cliente = ?"
        self.db.execute_query(query, (nombre, telefono, direccion, id_cliente))
        print(f"[v0] Cliente {id_cliente} actualizado")
    
    def eliminar(self, id_cliente: int):
        """Elimina un cliente"""
        query = "DELETE FROM Cliente WHERE ID_Cliente = ?"
        self.db.execute_query(query, (id_cliente,))
        print(f"[v0] Cliente {id_cliente} eliminado")
