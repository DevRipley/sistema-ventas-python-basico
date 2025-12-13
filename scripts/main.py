from database import Database
from cliente import Cliente
from proveedor import Proveedor
from producto import Producto
from empleado import Empleado
from venta import Venta

def inicializar_base_datos():
    """Inicializa la base de datos ejecutando el script SQL"""
    print("=== Inicializando Base de Datos ===")
    db = Database()
    db.execute_script("scripts/01_crear_base_datos.sql")
    print("✓ Base de datos creada exitosamente\n")

def cargar_datos_prueba():
    """Carga datos de prueba en la base de datos"""
    print("=== Cargando Datos de Prueba ===")
    db = Database()
    
    # Crear clientes
    cliente_mgr = Cliente(db)
    cliente1 = cliente_mgr.crear("Juan Pérez", "555-1234", "Calle Principal 123")
    cliente2 = cliente_mgr.crear("María González", "555-5678", "Avenida Central 456")
    
    # Crear proveedores
    proveedor_mgr = Proveedor(db)
    proveedor1 = proveedor_mgr.crear("Distribuidora ABC", "555-9999", "Zona Industrial")
    proveedor2 = proveedor_mgr.crear("Importadora XYZ", "555-8888", "Puerto Comercial")
    
    # Crear empleados
    empleado_mgr = Empleado(db)
    empleado1 = empleado_mgr.crear("Carlos Rodríguez", "Vendedor")
    empleado2 = empleado_mgr.crear("Ana Martínez", "Gerente de Ventas")
    
    # Crear productos
    producto_mgr = Producto(db)
    producto1 = producto_mgr.crear("Laptop Dell", "Electrónica", 899.99, 15, proveedor1)
    producto2 = producto_mgr.crear("Mouse Inalámbrico", "Electrónica", 25.50, 50, proveedor1)
    producto3 = producto_mgr.crear("Teclado Mecánico", "Electrónica", 75.00, 30, proveedor2)
    producto4 = producto_mgr.crear("Monitor 24\"", "Electrónica", 199.99, 20, proveedor2)
    
    print("✓ Datos de prueba cargados exitosamente\n")
    
    return {
        'clientes': [cliente1, cliente2],
        'empleados': [empleado1, empleado2],
        'productos': [producto1, producto2, producto3, producto4]
    }

def realizar_venta_ejemplo(datos):
    """Realiza una venta de ejemplo"""
    print("=== Realizando Venta de Ejemplo ===")
    db = Database()
    venta_mgr = Venta(db)
    
    # Venta: Cliente 1 compra 2 laptops y 5 mouses
    detalles = [
        (datos['productos'][0], 2, 899.99),  # 2 Laptops
        (datos['productos'][1], 5, 25.50),   # 5 Mouses
    ]
    
    venta_id = venta_mgr.crear(
        id_cliente=datos['clientes'][0],
        id_empleado=datos['empleados'][0],
        detalles=detalles
    )
    
    print(f"✓ Venta registrada con ID: {venta_id}")
    total = venta_mgr.calcular_total(venta_id)
    print(f"✓ Total de la venta: ${total:.2f}\n")
    
    return venta_id

def mostrar_reportes(venta_id):
    """Muestra reportes del sistema"""
    print("=== Reportes del Sistema ===")
    db = Database()
    
    # Mostrar clientes
    print("\n--- Clientes ---")
    cliente_mgr = Cliente(db)
    clientes = cliente_mgr.listar()
    for cliente in clientes:
        print(f"ID: {cliente['ID_Cliente']}, Nombre: {cliente['Nombre']}, Teléfono: {cliente['Telefono']}")
    
    # Mostrar productos con stock
    print("\n--- Productos (con stock actualizado) ---")
    producto_mgr = Producto(db)
    productos = producto_mgr.listar()
    for producto in productos:
        print(f"ID: {producto['ID_Producto']}, Nombre: {producto['Nombre']}, "
              f"Precio: ${producto['Precio']:.2f}, Stock: {producto['Stock']}")
    
    # Mostrar ventas
    print("\n--- Ventas ---")
    venta_mgr = Venta(db)
    ventas = venta_mgr.listar()
    for venta in ventas:
        total = venta_mgr.calcular_total(venta['ID_Venta'])
        print(f"ID: {venta['ID_Venta']}, Fecha: {venta['Fecha']}, "
              f"Cliente: {venta['Cliente']}, Empleado: {venta['Empleado']}, "
              f"Total: ${total:.2f}")
    
    # Mostrar detalle de la venta realizada
    print(f"\n--- Detalle de Venta #{venta_id} ---")
    detalles = venta_mgr.obtener_detalles(venta_id)
    for detalle in detalles:
        subtotal = detalle['Cantidad'] * detalle['Precio_Unitario']
        print(f"Producto: {detalle['Producto']}, "
              f"Cantidad: {detalle['Cantidad']}, "
              f"Precio: ${detalle['Precio_Unitario']:.2f}, "
              f"Subtotal: ${subtotal:.2f}")

def main():
    """Función principal del sistema"""
    print("╔════════════════════════════════════════╗")
    print("║   SISTEMA DE VENTAS - DEMO COMPLETO   ║")
    print("╚════════════════════════════════════════╝\n")
    
    # Paso 1: Inicializar base de datos
    inicializar_base_datos()
    
    # Paso 2: Cargar datos de prueba
    datos = cargar_datos_prueba()
    
    # Paso 3: Realizar una venta
    venta_id = realizar_venta_ejemplo(datos)
    
    # Paso 4: Mostrar reportes
    mostrar_reportes(venta_id)
    
    print("\n╔════════════════════════════════════════╗")
    print("║        DEMO FINALIZADA CON ÉXITO       ║")
    print("╚════════════════════════════════════════╝")

if __name__ == "__main__":
    main()
