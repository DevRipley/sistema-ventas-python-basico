from database import Database

class Producto:
    """Clase para gestionar productos"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def crear(self, nombre: str, categoria: str, precio: float, stock: int, proveedor_id: int = None):
        """Crea un nuevo producto"""
        query = "INSERT INTO Producto (Nombre, Categoria, Precio, Stock, Proveedor_ID) VALUES (?, ?, ?, ?, ?)"
        producto_id = self.db.execute_query(query, (nombre, categoria, precio, stock, proveedor_id))
        print(f"[v0] Producto creado con ID: {producto_id}")
        return producto_id
    
    def obtener(self, id_producto: int):
        """Obtiene un producto por ID"""
        query = "SELECT * FROM Producto WHERE ID_Producto = ?"
        return self.db.fetch_one(query, (id_producto,))
    
    def listar(self):
        """Lista todos los productos"""
        query = "SELECT * FROM Producto"
        return self.db.fetch_all(query)
    
    def listar_con_stock(self):
        """Lista productos con stock disponible"""
        query = "SELECT * FROM Producto WHERE Stock > 0"
        return self.db.fetch_all(query)
    
    def actualizar(self, id_producto: int, nombre: str, categoria: str, precio: float, stock: int, proveedor_id: int = None):
        """Actualiza un producto"""
        query = "UPDATE Producto SET Nombre = ?, Categoria = ?, Precio = ?, Stock = ?, Proveedor_ID = ? WHERE ID_Producto = ?"
        self.db.execute_query(query, (nombre, categoria, precio, stock, proveedor_id, id_producto))
        print(f"[v0] Producto {id_producto} actualizado")
    
    def actualizar_stock(self, id_producto: int, cantidad: int):
        """Actualiza el stock de un producto (reduce el stock)"""
        query = "UPDATE Producto SET Stock = Stock - ? WHERE ID_Producto = ?"
        self.db.execute_query(query, (cantidad, id_producto))
        print(f"[v0] Stock del producto {id_producto} reducido en {cantidad}")
    
    def eliminar(self, id_producto: int):
        """Elimina un producto"""
        query = "DELETE FROM Producto WHERE ID_Producto = ?"
        self.db.execute_query(query, (id_producto,))
        print(f"[v0] Producto {id_producto} eliminado")
