from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'Manual de Usuario - Sistema de Ventas', ln=True, align='C')
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

    def chapter_title(self, label):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 51, 102)
        self.cell(0, 8, label, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def chapter_body(self, text):
        self.set_font('Helvetica', '', 11)
        self.multi_cell(0, 6, text)
        self.ln(4)

    def add_list(self, items):
        self.set_font('Helvetica', '', 11)
        for item in items:
            self.multi_cell(180, 6, f'- {item}')
        self.ln(3)

    def add_table(self, rows, col_widths):
        self.set_font('Helvetica', '', 10)
        for row in rows:
            for i, cell in enumerate(row):
                self.multi_cell(col_widths[i], 6, cell, border=1, ln=3 if i == len(row)-1 else 0)
            self.ln(0)
        self.ln(4)

pdf = PDF()
pdf.set_auto_page_break(True, margin=15)
pdf.add_page()

pdf.chapter_title('1. Visión general')
pdf.chapter_body(
    'Este sistema de ventas es una aplicación de escritorio escrita en Python que permite gestionar clientes, ' 
    'proveedores, productos, empleados y ventas mediante una interfaz gráfica basada en Tkinter. ' 
    'La base de datos se guarda en SQLite y el sistema incluye roles de usuario para administración.'
)

pdf.chapter_title('2. Requisitos')
pdf.add_list([
    'Python 3.8+ con Tkinter disponible.',
    'Base de datos SQLite incluida en el archivo sistema_ventas.db o generada automáticamente.',
    'Ejecutar desde la carpeta del proyecto o desde el subdirectorio scripts.',
])

pdf.chapter_title('3. Inicio de la aplicación')
pdf.chapter_body(
    'Abra una terminal y ejecute el archivo principal del proyecto. Desde la carpeta raíz del proyecto:'
)
pdf.set_font('Courier', '', 10)
pdf.multi_cell(0, 6, 'python scripts/main.py')
pdf.ln(3)
pdf.set_font('Helvetica', '', 11)
pdf.chapter_body(
    'Al iniciar, la aplicación muestra una pantalla de inicio de sesión. Si no existe un administrador, el sistema crea automáticamente ' 
    'un usuario por defecto con las siguientes credenciales:'
)
pdf.add_list([
    'Usuario: admin',
    'Contraseña: admin123',
])

pdf.chapter_title('4. Pantalla de inicio de sesión')
pdf.chapter_body(
    'Ingrese el nombre de usuario y la contraseña para acceder. Si las credenciales son correctas, se abre la interfaz principal. ' 
    'Si los campos quedan vacíos, se solicita completarlos.'
)

pdf.chapter_title('5. Navegación principal')
pdf.chapter_body(
    'La interfaz principal utiliza pestañas para separar las funciones de gestión. Las pestañas disponibles son:'
)
pdf.add_list([
    'Clientes',
    'Empleados (solo para administradores)',
    'Productos',
    'Proveedores',
    'Ventas',
    'Reportes',
])

pdf.chapter_title('6. Gestión de clientes')
pdf.chapter_body(
    'En la pestaña Clientes puede crear, actualizar, eliminar y listar clientes. ' 
    'Para crear un cliente, ingrese Nombre, Teléfono y Dirección y presione Crear. ' 
    'Para actualizar o eliminar, seleccione una fila de la tabla con doble clic y luego use los botones apropiados.'
)

pdf.chapter_title('7. Gestión de empleados')
pdf.chapter_body(
    'Solo los usuarios con rol admin pueden acceder a esta pestaña. Permite crear, actualizar y eliminar empleados. ' 
    'Los campos obligatorios para un nuevo empleado son Nombre, Usuario, Contraseña y Rol.'
)

pdf.chapter_title('8. Gestión de productos')
pdf.chapter_body(
    'En Productos puede crear nuevas referencias con nombre, categoría, precio, stock y proveedor asociado. ' 
    'También puede actualizar o eliminar productos existentes desde la lista.'
)

pdf.chapter_title('9. Gestión de proveedores')
pdf.chapter_body(
    'En Proveedores se registran los datos de los proveedores. Los campos son Nombre, Teléfono y Dirección. ' 
    'Luego se pueden asociar proveedores a productos.'
)

pdf.chapter_title('10. Ventas')
pdf.chapter_body(
    'La pestaña Ventas permite registrar transacciones reales. Para realizar una venta:'
)
pdf.add_list([
    'Seleccione un cliente.',
    'Seleccione un producto disponible en stock.',
    'Ingrese la cantidad deseada y presione Agregar al Carrito.',
    'Repita hasta completar los productos de la venta.',
    'Presione Realizar Venta para cerrar la transacción.',
])
pdf.chapter_body(
    'La aplicación verifica el stock antes de agregar el producto y actualiza el inventario al confirmar la venta. ' 
    'Si el carrito está vacío, no se permite realizar la venta.'
)

pdf.chapter_title('11. Reportes')
pdf.chapter_body(
    'La pestaña Reportes genera un resumen completo de clientes, empleados, productos, proveedores y ventas. ' 
    'Presione Generar Reporte Completo para ver todos los datos en pantalla.'
)

pdf.chapter_title('12. Base de datos y archivos')
pdf.chapter_body(
    'El proyecto usa una base de datos SQLite ubicada en el archivo sistema_ventas.db. La estructura se define en scripts/01_crear_base_datos.sql. ' 
    'Si se ejecuta por primera vez, el sistema crea las tablas necesarias automáticamente. ' 
    'El archivo scripts/02_migrar_empleados.sql contiene la lógica de migración para agregar columnas de usuario y rol a la tabla Empleado.'
)

pdf.chapter_title('13. Recomendaciones de uso')
pdf.add_list([
    'No elimine el archivo sistema_ventas.db si desea conservar los datos.',
    'Use el usuario admin solo para administrar empleados y configuración.',
    'Registre proveedores antes de asignarlos a productos.',
    'Verifique el stock antes de vender para evitar errores.',
])

pdf.chapter_title('14. Consideraciones importantes')
pdf.chapter_body(
    'Eliminar una venta no restaura el stock del producto. La aplicación guarda los datos permanentemente en SQLite. ' 
    'El sistema usa SHA256 para almacenar contraseñas de empleados.'
)

output_path = 'Manual_de_Usuario_Sistema_Ventas.pdf'
pdf.output(output_path)
print(f'Manual generado en: {output_path}')
