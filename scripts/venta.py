from database import Database
from datetime import datetime

class Venta:
    """Clase para gestionar ventas"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def crear(self, id_cliente: int, id_empleado: int, detalles: list):
        """
        Crea una nueva venta con sus detalles
        detalles: lista de tuplas (id_producto, cantidad, precio_unitario)
        """
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Crear la venta
        query_venta = "INSERT INTO Venta (Fecha, ID_Cliente, ID_Empleado) VALUES (?, ?, ?)"
        venta_id = self.db.execute_query(query_venta, (fecha, id_cliente, id_empleado))
        
        # Crear los detalles de la venta y actualizar stock
        query_detalle = "INSERT INTO Detalle_Venta (ID_Venta, ID_Producto, Cantidad, Precio_Unitario) VALUES (?, ?, ?, ?)"
        query_stock = "UPDATE Producto SET Stock = Stock - ? WHERE ID_Producto = ?"
        
        conn = self.db.connect()
        cursor = conn.cursor()
        
        for id_producto, cantidad, precio_unitario in detalles:
            # Verificar stock disponible
            cursor.execute("SELECT Stock FROM Producto WHERE ID_Producto = ?", (id_producto,))
            stock_actual = cursor.fetchone()[0]
            
            if stock_actual < cantidad:
                conn.rollback()
                self.db.disconnect()
                raise ValueError(f"Stock insuficiente para producto {id_producto}. Disponible: {stock_actual}, Solicitado: {cantidad}")
            
            # Insertar detalle
            cursor.execute(query_detalle, (venta_id, id_producto, cantidad, precio_unitario))
            
            # Actualizar stock
            cursor.execute(query_stock, (cantidad, id_producto))
        
        conn.commit()
        self.db.disconnect()
        
        print(f"[v0] Venta creada con ID: {venta_id}")
        return venta_id
    
    def obtener(self, id_venta: int):
        """Obtiene una venta por ID"""
        query = """
        SELECT v.*, c.Nombre as Cliente, e.Nombre as Empleado
        FROM Venta v
        JOIN Cliente c ON v.ID_Cliente = c.ID_Cliente
        JOIN Empleado e ON v.ID_Empleado = e.ID_Empleado
        WHERE v.ID_Venta = ?
        """
        return self.db.fetch_one(query, (id_venta,))
    
    def obtener_detalles(self, id_venta: int):
        """Obtiene los detalles de una venta"""
        query = """
        SELECT dv.*, p.Nombre as Producto
        FROM Detalle_Venta dv
        JOIN Producto p ON dv.ID_Producto = p.ID_Producto
        WHERE dv.ID_Venta = ?
        """
        return self.db.fetch_all(query, (id_venta,))
    
    def listar(self):
        """Lista todas las ventas"""
        query = """
        SELECT v.*, c.Nombre as Cliente, e.Nombre as Empleado
        FROM Venta v
        JOIN Cliente c ON v.ID_Cliente = c.ID_Cliente
        JOIN Empleado e ON v.ID_Empleado = e.ID_Empleado
        ORDER BY v.Fecha DESC
        """
        return self.db.fetch_all(query)
    
    def calcular_total(self, id_venta: int):
        """Calcula el total de una venta"""
        query = """
        SELECT SUM(Cantidad * Precio_Unitario) as Total
        FROM Detalle_Venta
        WHERE ID_Venta = ?
        """
        result = self.db.fetch_one(query, (id_venta,))
        return result[0] if result and result[0] else 0
    
    def eliminar(self, id_venta: int):
        """Elimina una venta (nota: esto no restaura el stock)"""
        query = "DELETE FROM Venta WHERE ID_Venta = ?"
        self.db.execute_query(query, (id_venta,))
        print(f"[v0] Venta {id_venta} eliminada")
