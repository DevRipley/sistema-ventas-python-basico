import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import Database
from cliente import Cliente
from empleado import Empleado
from producto import Producto
from proveedor import Proveedor
from venta import Venta
from datetime import datetime

class SistemaVentasGUI:
    def __init__(self, root, empleado_logueado):
        self.root = root
        self.empleado_logueado = empleado_logueado
        self.root.title(f"Mi propio esfuerzo - {empleado_logueado['Nombre']}")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Configurar tema moderno
        self.configurar_tema()
        
        # Inicializar base de datos
        self.db = Database()
        
        # Inicializar managers
        self.cliente_mgr = Cliente(self.db)
        self.empleado_mgr = Empleado(self.db)
        self.producto_mgr = Producto(self.db)
        self.proveedor_mgr = Proveedor(self.db)
        self.venta_mgr = Venta(self.db)
        
        # Variables para ventas
        self.carrito_venta = []
        
        # Verificar si es admin
        self.es_admin = (empleado_logueado['Rol'] if 'Rol' in empleado_logueado.keys() else 'empleado') == 'admin'
        
        self.crear_interfaz()
        self.cargar_datos_iniciales()
        
        # Crear barra de menú con logout
        self.crear_menu()
    
    def configurar_tema(self):
        """Configura un tema moderno para la aplicación"""
        style = ttk.Style()
        
        # Intentar usar un tema moderno
        temas_disponibles = style.theme_names()
        if 'vista' in temas_disponibles:
            style.theme_use('vista')
        elif 'clam' in temas_disponibles:
            style.theme_use('clam')
        else:
            style.theme_use('default')
        
        # Colores modernos
        colores = {
            'bg_principal': '#ffffff',
            'bg_secundario': '#f5f5f5',
            'bg_terciario': '#e8e8e8',
            'accent': '#0078d4',
            'accent_hover': '#005a9e',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'text_primary': '#212529',
            'text_secondary': '#6c757d',
            'border': '#dee2e6'
        }
        
        # Configurar Notebook (pestañas)
        style.configure('TNotebook', background=colores['bg_secundario'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[20, 10], 
                       background=colores['bg_terciario'],
                       foreground=colores['text_primary'],
                       borderwidth=1,
                       relief='flat')
        style.map('TNotebook.Tab',
                 background=[('selected', colores['accent']),
                           ('active', colores['accent_hover'])],
                 foreground=[('selected', '#000000'),
                           ('active', '#000000')])
        
        # Configurar Frames
        style.configure('TFrame', background=colores['bg_principal'])
        style.configure('TLabelframe', background=colores['bg_principal'], 
                        foreground=colores['text_primary'], borderwidth=1)
        style.configure('TLabelframe.Label', background=colores['bg_principal'],
                       foreground=colores['accent'], font=('Segoe UI', 10, 'bold'))
        
        # Configurar Botones
        style.configure('TButton', 
                       padding=[15, 8],
                       font=('Segoe UI', 9),
                       borderwidth=0,
                       relief='flat',
                       background=colores['accent'],
                       foreground='#000000')
        style.map('TButton',
                 background=[('active', colores['accent_hover']),
                           ('pressed', colores['accent_hover'])],
                 foreground=[('active', '#000000'),
                           ('pressed', '#000000')])
        
        # Botón de éxito
        style.configure('Success.TButton',
                       background=colores['success'],
                       foreground='#000000')
        style.map('Success.TButton',
                 background=[('active', '#218838'),
                           ('pressed', '#1e7e34')],
                 foreground=[('active', '#000000'),
                           ('pressed', '#000000')])
        
        # Botón de peligro
        style.configure('Danger.TButton',
                       background=colores['danger'],
                       foreground='#000000')
        style.map('Danger.TButton',
                 background=[('active', '#c82333'),
                           ('pressed', '#bd2130')],
                 foreground=[('active', '#000000'),
                           ('pressed', '#000000')])
        
        # Configurar Entries
        style.configure('TEntry',
                       fieldbackground=colores['bg_principal'],
                       borderwidth=1,
                       relief='solid',
                       padding=8,
                       font=('Segoe UI', 9))
        style.map('TEntry',
                 bordercolor=[('focus', colores['accent'])],
                 lightcolor=[('focus', colores['accent'])],
                 darkcolor=[('focus', colores['accent'])])
        
        # Configurar Combobox
        style.configure('TCombobox',
                       fieldbackground=colores['bg_principal'],
                       borderwidth=1,
                       relief='solid',
                       padding=8,
                       font=('Segoe UI', 9))
        style.map('TCombobox',
                 bordercolor=[('focus', colores['accent'])],
                 lightcolor=[('focus', colores['accent'])],
                 darkcolor=[('focus', colores['accent'])])
        
        # Configurar Treeview
        style.configure('Treeview',
                       background=colores['bg_principal'],
                       foreground=colores['text_primary'],
                       fieldbackground=colores['bg_principal'],
                       borderwidth=1,
                       font=('Segoe UI', 9))
        style.configure('Treeview.Heading',
                       background=colores['accent'],
                       foreground='#000000',
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat',
                       borderwidth=0)
        style.map('Treeview',
                 background=[('selected', colores['accent'])],
                 foreground=[('selected', '#ffffff')])
        
        # Configurar Labels
        style.configure('TLabel',
                       background=colores['bg_principal'],
                       foreground=colores['text_primary'],
                       font=('Segoe UI', 9))
        style.configure('Title.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=colores['accent'])
        
        # Configurar Scrollbar
        style.configure('TScrollbar',
                       background=colores['bg_terciario'],
                       troughcolor=colores['bg_secundario'],
                       borderwidth=0,
                       arrowcolor=colores['text_secondary'],
                       darkcolor=colores['bg_terciario'],
                       lightcolor=colores['bg_terciario'])
        
        # Configurar fondo de la ventana
        self.root.configure(bg=colores['bg_secundario'])
        
        # Guardar colores para uso posterior
        self.colores = colores
    
    def crear_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú de usuario
        usuario_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=f"Usuario: {self.empleado_logueado['Nombre']}", menu=usuario_menu)
        usuario_menu.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        
        # Crédito escondido - menú de ayuda
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="?", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de...", command=self.mostrar_acerca_de)
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de cerrar sesión?"):
            self.root.destroy()
            # Reiniciar aplicación con login
            import sys
            import os
            python = sys.executable
            os.execl(python, python, *sys.argv)
    
    def mostrar_acerca_de(self):
        """Muestra información sobre el sistema"""
        # Crédito escondido
        mensaje = "Mi propio esfuerzo\n\n"
        mensaje += "Sistema de gestión de ventas\n\n"
        mensaje += "Versión 1.0\n\n"
        mensaje += "helped with Purpura Development"
        messagebox.showinfo("Acerca de", mensaje)
    
    def crear_interfaz(self):
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestañas
        self.crear_pestaña_clientes()
        if self.es_admin:
            self.crear_pestaña_empleados()
        self.crear_pestaña_productos()
        self.crear_pestaña_proveedores()
        self.crear_pestaña_ventas()
        self.crear_pestaña_reportes()
    
    def crear_pestaña_clientes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👥 Clientes")
        
        # Frame superior - Formulario
        form_frame = ttk.LabelFrame(frame, text="Gestión de Clientes", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cliente_nombre = ttk.Entry(form_frame, width=30)
        self.cliente_nombre.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Teléfono:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cliente_telefono = ttk.Entry(form_frame, width=30)
        self.cliente_telefono.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Dirección:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cliente_direccion = ttk.Entry(form_frame, width=30)
        self.cliente_direccion.grid(row=2, column=1, pady=5, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Crear", command=self.crear_cliente, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_cliente, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario_cliente).pack(side=tk.LEFT, padx=5)
        
        # Frame inferior - Tabla
        table_frame = ttk.LabelFrame(frame, text="Lista de Clientes", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("ID", "Nombre", "Teléfono", "Dirección")
        self.tree_clientes = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_clientes.bind("<Double-1>", self.seleccionar_cliente)
    
    def crear_pestaña_empleados(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👤 Empleados")
        
        # Frame superior - Formulario
        form_frame = ttk.LabelFrame(frame, text="Gestión de Empleados (Solo Administradores)", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.empleado_nombre = ttk.Entry(form_frame, width=30)
        self.empleado_nombre.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Cargo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.empleado_cargo = ttk.Entry(form_frame, width=30)
        self.empleado_cargo.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Usuario:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.empleado_usuario = ttk.Entry(form_frame, width=30)
        self.empleado_usuario.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.empleado_contrasena = ttk.Entry(form_frame, width=30, show="*")
        self.empleado_contrasena.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Rol:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.empleado_rol = ttk.Combobox(form_frame, width=27, state="readonly", values=["admin", "empleado"])
        self.empleado_rol.grid(row=4, column=1, pady=5, padx=5)
        self.empleado_rol.set("empleado")
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Crear", command=self.crear_empleado, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_empleado).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_empleado, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario_empleado).pack(side=tk.LEFT, padx=5)
        
        # Frame inferior - Tabla
        table_frame = ttk.LabelFrame(frame, text="Lista de Empleados", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("ID", "Nombre", "Cargo", "Usuario", "Rol")
        self.tree_empleados = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree_empleados.heading(col, text=col)
            self.tree_empleados.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_empleados.yview)
        self.tree_empleados.configure(yscrollcommand=scrollbar.set)
        
        self.tree_empleados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_empleados.bind("<Double-1>", self.seleccionar_empleado)
    
    def crear_pestaña_productos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📦 Productos")
        
        # Frame superior - Formulario
        form_frame = ttk.LabelFrame(frame, text="Gestión de Productos", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.producto_nombre = ttk.Entry(form_frame, width=30)
        self.producto_nombre.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Categoría:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.producto_categoria = ttk.Entry(form_frame, width=30)
        self.producto_categoria.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Precio:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.producto_precio = ttk.Entry(form_frame, width=30)
        self.producto_precio.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Stock:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.producto_stock = ttk.Entry(form_frame, width=30)
        self.producto_stock.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Proveedor:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.producto_proveedor = ttk.Combobox(form_frame, width=27, state="readonly")
        self.producto_proveedor.grid(row=4, column=1, pady=5, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Crear", command=self.crear_producto, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_producto, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario_producto).pack(side=tk.LEFT, padx=5)
        
        # Frame inferior - Tabla
        table_frame = ttk.LabelFrame(frame, text="Lista de Productos", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("ID", "Nombre", "Categoría", "Precio", "Stock", "Proveedor")
        self.tree_productos = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_productos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_productos.bind("<Double-1>", self.seleccionar_producto)
    
    def crear_pestaña_proveedores(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏢 Proveedores")
        
        # Frame superior - Formulario
        form_frame = ttk.LabelFrame(frame, text="Gestión de Proveedores", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.proveedor_nombre = ttk.Entry(form_frame, width=30)
        self.proveedor_nombre.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Teléfono:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.proveedor_telefono = ttk.Entry(form_frame, width=30)
        self.proveedor_telefono.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Dirección:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.proveedor_direccion = ttk.Entry(form_frame, width=30)
        self.proveedor_direccion.grid(row=2, column=1, pady=5, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Crear", command=self.crear_proveedor, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_proveedor).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_proveedor, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario_proveedor).pack(side=tk.LEFT, padx=5)
        
        # Frame inferior - Tabla
        table_frame = ttk.LabelFrame(frame, text="Lista de Proveedores", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("ID", "Nombre", "Teléfono", "Dirección")
        self.tree_proveedores = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree_proveedores.heading(col, text=col)
            self.tree_proveedores.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_proveedores.yview)
        self.tree_proveedores.configure(yscrollcommand=scrollbar.set)
        
        self.tree_proveedores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_proveedores.bind("<Double-1>", self.seleccionar_proveedor)
    
    def crear_pestaña_ventas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💰 Ventas")
        
        # Frame izquierdo - Formulario de venta
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        form_frame = ttk.LabelFrame(left_frame, text="Nueva Venta", padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mostrar empleado logueado
        ttk.Label(form_frame, text="Empleado:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        cargo = self.empleado_logueado['Cargo'] if 'Cargo' in self.empleado_logueado.keys() and self.empleado_logueado['Cargo'] else 'N/A'
        ttk.Label(form_frame, text=f"{self.empleado_logueado['Nombre']} ({cargo})", 
                 font=("Arial", 9)).grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Cliente:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.venta_cliente = ttk.Combobox(form_frame, width=30, state="readonly")
        self.venta_cliente.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Producto:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.venta_producto = ttk.Combobox(form_frame, width=30, state="readonly")
        self.venta_producto.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Cantidad:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.venta_cantidad = ttk.Entry(form_frame, width=30)
        self.venta_cantidad.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Button(form_frame, text="Agregar al Carrito", command=self.agregar_al_carrito, style='Success.TButton').grid(row=4, column=0, columnspan=2, pady=10)
        
        # Carrito
        carrito_frame = ttk.LabelFrame(left_frame, text="Carrito de Compra", padding=10)
        carrito_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns_carrito = ("Producto", "Cantidad", "Precio Unit.", "Subtotal")
        self.tree_carrito = ttk.Treeview(carrito_frame, columns=columns_carrito, show="headings", height=8)
        
        for col in columns_carrito:
            self.tree_carrito.heading(col, text=col)
            self.tree_carrito.column(col, width=120)
        
        scrollbar_carrito = ttk.Scrollbar(carrito_frame, orient=tk.VERTICAL, command=self.tree_carrito.yview)
        self.tree_carrito.configure(yscrollcommand=scrollbar_carrito.set)
        
        self.tree_carrito.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_carrito.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Total
        total_frame = ttk.Frame(left_frame)
        total_frame.pack(fill=tk.X, pady=5)
        
        self.label_total = ttk.Label(total_frame, text="Total: $0.00", font=("Segoe UI", 16, "bold"), style='Title.TLabel')
        self.label_total.pack()
        
        btn_frame_venta = ttk.Frame(left_frame)
        btn_frame_venta.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame_venta, text="Realizar Venta", command=self.realizar_venta, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame_venta, text="Limpiar Carrito", command=self.limpiar_carrito, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        # Frame derecho - Historial de ventas
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        table_frame = ttk.LabelFrame(right_frame, text="Historial de Ventas", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns_ventas = ("ID", "Fecha", "Cliente", "Empleado", "Total")
        self.tree_ventas = ttk.Treeview(table_frame, columns=columns_ventas, show="headings", height=20)
        
        for col in columns_ventas:
            self.tree_ventas.heading(col, text=col)
            self.tree_ventas.column(col, width=150)
        
        scrollbar_ventas = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar_ventas.set)
        
        self.tree_ventas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_ventas.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_ventas.bind("<Double-1>", self.ver_detalle_venta)
    
    def crear_pestaña_reportes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Reportes")
        
        # Área de texto para reportes
        reporte_frame = ttk.LabelFrame(frame, text="Reportes del Sistema", padding=10)
        reporte_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_reporte = scrolledtext.ScrolledText(reporte_frame, height=30, width=80, wrap=tk.WORD)
        self.text_reporte.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Generar Reporte Completo", command=self.generar_reporte_completo, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.text_reporte.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
    
    # Métodos para Clientes
    def crear_cliente(self):
        try:
            nombre = self.cliente_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            self.cliente_mgr.crear(
                nombre,
                self.cliente_telefono.get().strip(),
                self.cliente_direccion.get().strip()
            )
            messagebox.showinfo("Éxito", "Cliente creado exitosamente")
            self.limpiar_formulario_cliente()
            self.actualizar_tabla_clientes()
            self.actualizar_comboboxes_venta()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear cliente: {str(e)}")
    
    def actualizar_cliente(self):
        try:
            seleccion = self.tree_clientes.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar")
                return
            
            item = self.tree_clientes.item(seleccion[0])
            cliente_id = item['values'][0]
            
            nombre = self.cliente_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            self.cliente_mgr.actualizar(
                cliente_id,
                nombre,
                self.cliente_telefono.get().strip(),
                self.cliente_direccion.get().strip()
            )
            messagebox.showinfo("Éxito", "Cliente actualizado exitosamente")
            self.limpiar_formulario_cliente()
            self.actualizar_tabla_clientes()
            self.actualizar_comboboxes_venta()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente: {str(e)}")
    
    def eliminar_cliente(self):
        try:
            seleccion = self.tree_clientes.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
                return
            
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
                item = self.tree_clientes.item(seleccion[0])
                cliente_id = item['values'][0]
                self.cliente_mgr.eliminar(cliente_id)
                messagebox.showinfo("Éxito", "Cliente eliminado exitosamente")
                self.actualizar_tabla_clientes()
                self.actualizar_comboboxes_venta()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
    
    def seleccionar_cliente(self, event):
        seleccion = self.tree_clientes.selection()
        if seleccion:
            item = self.tree_clientes.item(seleccion[0])
            valores = item['values']
            self.cliente_nombre.delete(0, tk.END)
            self.cliente_nombre.insert(0, valores[1])
            self.cliente_telefono.delete(0, tk.END)
            self.cliente_telefono.insert(0, valores[2] if len(valores) > 2 else "")
            self.cliente_direccion.delete(0, tk.END)
            self.cliente_direccion.insert(0, valores[3] if len(valores) > 3 else "")
    
    def limpiar_formulario_cliente(self):
        self.cliente_nombre.delete(0, tk.END)
        self.cliente_telefono.delete(0, tk.END)
        self.cliente_direccion.delete(0, tk.END)
    
    def actualizar_tabla_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        clientes = self.cliente_mgr.listar()
        for cliente in clientes:
            self.tree_clientes.insert("", tk.END, values=(
                cliente['ID_Cliente'],
                cliente['Nombre'],
                cliente['Telefono'] or "",
                cliente['Direccion'] or ""
            ))
    
    # Métodos para Empleados
    def crear_empleado(self):
        if not self.es_admin:
            messagebox.showerror("Error", "Solo los administradores pueden crear empleados")
            return
        
        try:
            nombre = self.empleado_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            usuario = self.empleado_usuario.get().strip()
            contrasena = self.empleado_contrasena.get()
            rol = self.empleado_rol.get()
            
            if not usuario or not contrasena:
                messagebox.showerror("Error", "Usuario y contraseña son obligatorios")
                return
            
            self.empleado_mgr.crear(
                nombre, 
                self.empleado_cargo.get().strip(),
                usuario,
                contrasena,
                rol
            )
            messagebox.showinfo("Éxito", "Empleado creado exitosamente")
            self.limpiar_formulario_empleado()
            self.actualizar_tabla_empleados()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear empleado: {str(e)}")
    
    def actualizar_empleado(self):
        if not self.es_admin:
            messagebox.showerror("Error", "Solo los administradores pueden actualizar empleados")
            return
        
        try:
            seleccion = self.tree_empleados.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un empleado para actualizar")
                return
            
            item = self.tree_empleados.item(seleccion[0])
            empleado_id = item['values'][0]
            
            nombre = self.empleado_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            usuario = self.empleado_usuario.get().strip()
            contrasena = self.empleado_contrasena.get()
            rol = self.empleado_rol.get()
            
            if usuario and contrasena:
                self.empleado_mgr.actualizar(
                    empleado_id, 
                    nombre, 
                    self.empleado_cargo.get().strip(),
                    usuario,
                    contrasena,
                    rol
                )
            elif usuario:
                self.empleado_mgr.actualizar(
                    empleado_id, 
                    nombre, 
                    self.empleado_cargo.get().strip(),
                    usuario,
                    None,
                    rol
                )
            else:
                self.empleado_mgr.actualizar(
                    empleado_id, 
                    nombre, 
                    self.empleado_cargo.get().strip(),
                    None,
                    None,
                    rol
                )
            
            messagebox.showinfo("Éxito", "Empleado actualizado exitosamente")
            self.limpiar_formulario_empleado()
            self.actualizar_tabla_empleados()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar empleado: {str(e)}")
    
    def eliminar_empleado(self):
        if not self.es_admin:
            messagebox.showerror("Error", "Solo los administradores pueden eliminar empleados")
            return
        
        try:
            seleccion = self.tree_empleados.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar")
                return
            
            item = self.tree_empleados.item(seleccion[0])
            empleado_id = item['values'][0]
            
            # No permitir eliminar al mismo usuario
            if empleado_id == self.empleado_logueado['ID_Empleado']:
                messagebox.showerror("Error", "No puede eliminar su propio usuario")
                return
            
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este empleado?"):
                self.empleado_mgr.eliminar(empleado_id)
                messagebox.showinfo("Éxito", "Empleado eliminado exitosamente")
                self.actualizar_tabla_empleados()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar empleado: {str(e)}")
    
    def seleccionar_empleado(self, event):
        seleccion = self.tree_empleados.selection()
        if seleccion:
            item = self.tree_empleados.item(seleccion[0])
            valores = item['values']
            self.empleado_nombre.delete(0, tk.END)
            self.empleado_nombre.insert(0, valores[1])
            self.empleado_cargo.delete(0, tk.END)
            self.empleado_cargo.insert(0, valores[2] if len(valores) > 2 else "")
            self.empleado_usuario.delete(0, tk.END)
            self.empleado_usuario.insert(0, valores[3] if len(valores) > 3 else "")
            self.empleado_contrasena.delete(0, tk.END)
            self.empleado_rol.set(valores[4] if len(valores) > 4 else "empleado")
    
    def limpiar_formulario_empleado(self):
        self.empleado_nombre.delete(0, tk.END)
        self.empleado_cargo.delete(0, tk.END)
        self.empleado_usuario.delete(0, tk.END)
        self.empleado_contrasena.delete(0, tk.END)
        self.empleado_rol.set("empleado")
    
    def actualizar_tabla_empleados(self):
        for item in self.tree_empleados.get_children():
            self.tree_empleados.delete(item)
        
        empleados = self.empleado_mgr.listar()
        for empleado in empleados:
            usuario = empleado['Usuario'] if 'Usuario' in empleado.keys() and empleado['Usuario'] else ""
            rol = empleado['Rol'] if 'Rol' in empleado.keys() and empleado['Rol'] else "empleado"
            self.tree_empleados.insert("", tk.END, values=(
                empleado['ID_Empleado'],
                empleado['Nombre'],
                empleado['Cargo'] or "",
                usuario,
                rol
            ))
    
    # Métodos para Productos
    def crear_producto(self):
        try:
            nombre = self.producto_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            precio = float(self.producto_precio.get() or 0)
            stock = int(self.producto_stock.get() or 0)
            
            proveedor_id = None
            if self.producto_proveedor.get():
                proveedor_id = int(self.producto_proveedor.get().split(" - ")[0])
            
            self.producto_mgr.crear(
                nombre,
                self.producto_categoria.get().strip(),
                precio,
                stock,
                proveedor_id
            )
            messagebox.showinfo("Éxito", "Producto creado exitosamente")
            self.limpiar_formulario_producto()
            self.actualizar_tabla_productos()
            self.actualizar_comboboxes_venta()
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear producto: {str(e)}")
    
    def actualizar_producto(self):
        try:
            seleccion = self.tree_productos.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un producto para actualizar")
                return
            
            item = self.tree_productos.item(seleccion[0])
            producto_id = item['values'][0]
            
            nombre = self.producto_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            precio = float(self.producto_precio.get() or 0)
            stock = int(self.producto_stock.get() or 0)
            
            proveedor_id = None
            if self.producto_proveedor.get():
                proveedor_id = int(self.producto_proveedor.get().split(" - ")[0])
            
            self.producto_mgr.actualizar(
                producto_id,
                nombre,
                self.producto_categoria.get().strip(),
                precio,
                stock,
                proveedor_id
            )
            messagebox.showinfo("Éxito", "Producto actualizado exitosamente")
            self.limpiar_formulario_producto()
            self.actualizar_tabla_productos()
            self.actualizar_comboboxes_venta()
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar producto: {str(e)}")
    
    def eliminar_producto(self):
        try:
            seleccion = self.tree_productos.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
                return
            
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
                item = self.tree_productos.item(seleccion[0])
                producto_id = item['values'][0]
                self.producto_mgr.eliminar(producto_id)
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente")
                self.actualizar_tabla_productos()
                self.actualizar_comboboxes_venta()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
    
    def seleccionar_producto(self, event):
        seleccion = self.tree_productos.selection()
        if seleccion:
            item = self.tree_productos.item(seleccion[0])
            valores = item['values']
            self.producto_nombre.delete(0, tk.END)
            self.producto_nombre.insert(0, valores[1])
            self.producto_categoria.delete(0, tk.END)
            self.producto_categoria.insert(0, valores[2] if len(valores) > 2 else "")
            self.producto_precio.delete(0, tk.END)
            self.producto_precio.insert(0, valores[3] if len(valores) > 3 else "")
            self.producto_stock.delete(0, tk.END)
            self.producto_stock.insert(0, valores[4] if len(valores) > 4 else "")
    
    def limpiar_formulario_producto(self):
        self.producto_nombre.delete(0, tk.END)
        self.producto_categoria.delete(0, tk.END)
        self.producto_precio.delete(0, tk.END)
        self.producto_stock.delete(0, tk.END)
        self.producto_proveedor.set("")
    
    def actualizar_tabla_productos(self):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        productos = self.producto_mgr.listar()
        proveedores = {p['ID_Proveedor']: p['Nombre'] for p in self.proveedor_mgr.listar()}
        
        for producto in productos:
            proveedor_nombre = proveedores.get(producto['Proveedor_ID'], "N/A")
            self.tree_productos.insert("", tk.END, values=(
                producto['ID_Producto'],
                producto['Nombre'],
                producto['Categoria'] or "",
                f"${producto['Precio']:.2f}",
                producto['Stock'],
                proveedor_nombre
            ))
    
    # Métodos para Proveedores
    def crear_proveedor(self):
        try:
            nombre = self.proveedor_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            self.proveedor_mgr.crear(
                nombre,
                self.proveedor_telefono.get().strip(),
                self.proveedor_direccion.get().strip()
            )
            messagebox.showinfo("Éxito", "Proveedor creado exitosamente")
            self.limpiar_formulario_proveedor()
            self.actualizar_tabla_proveedores()
            self.actualizar_combobox_proveedores()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear proveedor: {str(e)}")
    
    def actualizar_proveedor(self):
        try:
            seleccion = self.tree_proveedores.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un proveedor para actualizar")
                return
            
            item = self.tree_proveedores.item(seleccion[0])
            proveedor_id = item['values'][0]
            
            nombre = self.proveedor_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            self.proveedor_mgr.actualizar(
                proveedor_id,
                nombre,
                self.proveedor_telefono.get().strip(),
                self.proveedor_direccion.get().strip()
            )
            messagebox.showinfo("Éxito", "Proveedor actualizado exitosamente")
            self.limpiar_formulario_proveedor()
            self.actualizar_tabla_proveedores()
            self.actualizar_combobox_proveedores()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar proveedor: {str(e)}")
    
    def eliminar_proveedor(self):
        try:
            seleccion = self.tree_proveedores.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar")
                return
            
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este proveedor?"):
                item = self.tree_proveedores.item(seleccion[0])
                proveedor_id = item['values'][0]
                self.proveedor_mgr.eliminar(proveedor_id)
                messagebox.showinfo("Éxito", "Proveedor eliminado exitosamente")
                self.actualizar_tabla_proveedores()
                self.actualizar_combobox_proveedores()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar proveedor: {str(e)}")
    
    def seleccionar_proveedor(self, event):
        seleccion = self.tree_proveedores.selection()
        if seleccion:
            item = self.tree_proveedores.item(seleccion[0])
            valores = item['values']
            self.proveedor_nombre.delete(0, tk.END)
            self.proveedor_nombre.insert(0, valores[1])
            self.proveedor_telefono.delete(0, tk.END)
            self.proveedor_telefono.insert(0, valores[2] if len(valores) > 2 else "")
            self.proveedor_direccion.delete(0, tk.END)
            self.proveedor_direccion.insert(0, valores[3] if len(valores) > 3 else "")
    
    def limpiar_formulario_proveedor(self):
        self.proveedor_nombre.delete(0, tk.END)
        self.proveedor_telefono.delete(0, tk.END)
        self.proveedor_direccion.delete(0, tk.END)
    
    def actualizar_tabla_proveedores(self):
        for item in self.tree_proveedores.get_children():
            self.tree_proveedores.delete(item)
        
        proveedores = self.proveedor_mgr.listar()
        for proveedor in proveedores:
            self.tree_proveedores.insert("", tk.END, values=(
                proveedor['ID_Proveedor'],
                proveedor['Nombre'],
                proveedor['Telefono'] or "",
                proveedor['Direccion'] or ""
            ))
    
    def actualizar_combobox_proveedores(self):
        proveedores = self.proveedor_mgr.listar()
        valores = [f"{p['ID_Proveedor']} - {p['Nombre']}" for p in proveedores]
        self.producto_proveedor['values'] = valores
    
    # Métodos para Ventas
    def agregar_al_carrito(self):
        try:
            producto_texto = self.venta_producto.get()
            if not producto_texto:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            
            cantidad = int(self.venta_cantidad.get() or 0)
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
            
            producto_id = int(producto_texto.split(" - ")[0])
            producto = self.producto_mgr.obtener(producto_id)
            
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            
            if producto['Stock'] < cantidad:
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto['Stock']}")
                return
            
            precio = producto['Precio']
            subtotal = precio * cantidad
            
            # Agregar al carrito
            self.carrito_venta.append({
                'id_producto': producto_id,
                'nombre': producto['Nombre'],
                'cantidad': cantidad,
                'precio': precio,
                'subtotal': subtotal
            })
            
            # Actualizar tabla del carrito
            self.tree_carrito.insert("", tk.END, values=(
                producto['Nombre'],
                cantidad,
                f"${precio:.2f}",
                f"${subtotal:.2f}"
            ))
            
            # Actualizar total
            self.actualizar_total()
            
            # Limpiar campos
            self.venta_cantidad.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def actualizar_total(self):
        total = sum(item['subtotal'] for item in self.carrito_venta)
        self.label_total.config(text=f"Total: ${total:.2f}")
    
    def limpiar_carrito(self):
        self.carrito_venta = []
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        self.actualizar_total()
    
    def realizar_venta(self):
        try:
            if not self.carrito_venta:
                messagebox.showwarning("Advertencia", "El carrito está vacío")
                return
            
            cliente_texto = self.venta_cliente.get()
            
            if not cliente_texto:
                messagebox.showerror("Error", "Seleccione un cliente")
                return
            
            cliente_id = int(cliente_texto.split(" - ")[0])
            empleado_id = self.empleado_logueado['ID_Empleado']
            
            # Preparar detalles
            detalles = [(item['id_producto'], item['cantidad'], item['precio']) for item in self.carrito_venta]
            
            # Crear venta
            venta_id = self.venta_mgr.crear(cliente_id, empleado_id, detalles)
            
            messagebox.showinfo("Éxito", f"Venta realizada exitosamente\nID de Venta: {venta_id}")
            
            # Limpiar formulario
            self.limpiar_carrito()
            self.venta_cliente.set("")
            self.venta_producto.set("")
            
            # Actualizar tablas
            self.actualizar_tabla_ventas()
            self.actualizar_tabla_productos()
            self.actualizar_comboboxes_venta()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar venta: {str(e)}")
    
    def ver_detalle_venta(self, event):
        seleccion = self.tree_ventas.selection()
        if seleccion:
            item = self.tree_ventas.item(seleccion[0])
            venta_id = item['values'][0]
            
            detalles = self.venta_mgr.obtener_detalles(venta_id)
            total = self.venta_mgr.calcular_total(venta_id)
            
            detalle_texto = f"Detalle de Venta #{venta_id}\n"
            detalle_texto += "=" * 50 + "\n"
            for detalle in detalles:
                subtotal = detalle['Cantidad'] * detalle['Precio_Unitario']
                detalle_texto += f"{detalle['Producto']}: {detalle['Cantidad']} x ${detalle['Precio_Unitario']:.2f} = ${subtotal:.2f}\n"
            detalle_texto += "=" * 50 + "\n"
            detalle_texto += f"Total: ${total:.2f}"
            
            messagebox.showinfo("Detalle de Venta", detalle_texto)
    
    def actualizar_tabla_ventas(self):
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        
        ventas = self.venta_mgr.listar()
        for venta in ventas:
            total = self.venta_mgr.calcular_total(venta['ID_Venta'])
            self.tree_ventas.insert("", tk.END, values=(
                venta['ID_Venta'],
                venta['Fecha'],
                venta['Cliente'],
                venta['Empleado'],
                f"${total:.2f}"
            ))
    
    def actualizar_comboboxes_venta(self):
        # Clientes
        clientes = self.cliente_mgr.listar()
        valores_clientes = [f"{c['ID_Cliente']} - {c['Nombre']}" for c in clientes]
        self.venta_cliente['values'] = valores_clientes
        
        # Productos con stock
        productos = self.producto_mgr.listar_con_stock()
        valores_productos = [f"{p['ID_Producto']} - {p['Nombre']} (Stock: {p['Stock']})" for p in productos]
        self.venta_producto['values'] = valores_productos
    
    # Métodos para Reportes
    def generar_reporte_completo(self):
        self.text_reporte.delete(1.0, tk.END)
        
        reporte = "=" * 60 + "\n"
        reporte += "REPORTE COMPLETO - MI PROPIO ESFUERZO\n"
        reporte += "=" * 60 + "\n\n"
        
        # Clientes
        reporte += "--- CLIENTES ---\n"
        clientes = self.cliente_mgr.listar()
        for cliente in clientes:
            reporte += f"ID: {cliente['ID_Cliente']} | Nombre: {cliente['Nombre']} | "
            reporte += f"Teléfono: {cliente['Telefono'] or 'N/A'} | "
            reporte += f"Dirección: {cliente['Direccion'] or 'N/A'}\n"
        reporte += f"Total de clientes: {len(clientes)}\n\n"
        
        # Empleados
        reporte += "--- EMPLEADOS ---\n"
        empleados = self.empleado_mgr.listar()
        for empleado in empleados:
            reporte += f"ID: {empleado['ID_Empleado']} | Nombre: {empleado['Nombre']} | "
            reporte += f"Cargo: {empleado['Cargo'] or 'N/A'}\n"
        reporte += f"Total de empleados: {len(empleados)}\n\n"
        
        # Productos
        reporte += "--- PRODUCTOS ---\n"
        productos = self.producto_mgr.listar()
        proveedores = {p['ID_Proveedor']: p['Nombre'] for p in self.proveedor_mgr.listar()}
        for producto in productos:
            proveedor_nombre = proveedores.get(producto['Proveedor_ID'], "N/A")
            reporte += f"ID: {producto['ID_Producto']} | Nombre: {producto['Nombre']} | "
            reporte += f"Categoría: {producto['Categoria'] or 'N/A'} | "
            reporte += f"Precio: ${producto['Precio']:.2f} | Stock: {producto['Stock']} | "
            reporte += f"Proveedor: {proveedor_nombre}\n"
        reporte += f"Total de productos: {len(productos)}\n\n"
        
        # Proveedores
        reporte += "--- PROVEEDORES ---\n"
        proveedores_list = self.proveedor_mgr.listar()
        for proveedor in proveedores_list:
            reporte += f"ID: {proveedor['ID_Proveedor']} | Nombre: {proveedor['Nombre']} | "
            reporte += f"Teléfono: {proveedor['Telefono'] or 'N/A'} | "
            reporte += f"Dirección: {proveedor['Direccion'] or 'N/A'}\n"
        reporte += f"Total de proveedores: {len(proveedores_list)}\n\n"
        
        # Ventas
        reporte += "--- VENTAS ---\n"
        ventas = self.venta_mgr.listar()
        total_general = 0
        for venta in ventas:
            total = self.venta_mgr.calcular_total(venta['ID_Venta'])
            total_general += total
            reporte += f"ID: {venta['ID_Venta']} | Fecha: {venta['Fecha']} | "
            reporte += f"Cliente: {venta['Cliente']} | Empleado: {venta['Empleado']} | "
            reporte += f"Total: ${total:.2f}\n"
        reporte += f"Total de ventas: {len(ventas)}\n"
        reporte += f"Total general: ${total_general:.2f}\n"
        
        self.text_reporte.insert(1.0, reporte)
    
    def cargar_datos_iniciales(self):
        # Actualizar todas las tablas
        self.actualizar_tabla_clientes()
        self.actualizar_tabla_empleados()
        self.actualizar_tabla_productos()
        self.actualizar_tabla_proveedores()
        self.actualizar_tabla_ventas()
        
        # Actualizar comboboxes
        self.actualizar_combobox_proveedores()
        self.actualizar_comboboxes_venta()

def main():
    root = tk.Tk()
    app = SistemaVentasGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

