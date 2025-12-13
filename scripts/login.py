import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from empleado import Empleado

class LoginWindow:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.empleado_logueado = None
        
        # Crear ventana de login como ventana principal
        self.window = root
        self.window.title("Iniciar Sesión - Mi propio esfuerzo")
        
        # Configurar tema moderno primero
        self.configurar_tema()
        
        # Obtener dimensiones de la pantalla
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Configurar ventana en pantalla completa sin decoraciones
        # Primero establecer geometría, luego quitar decoraciones
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.window.overrideredirect(True)  # Sin decoraciones (sin barra de título, botones, etc.)
        
        # Inicializar base de datos
        self.db = Database()
        self.empleado_mgr = Empleado(self.db)
        
        # Verificar si existe un admin, si no, crear uno por defecto
        self.verificar_admin_por_defecto()
        
        self.crear_interfaz()
        
        # Enfocar en el campo de usuario
        self.entry_usuario.focus()
        
        # Bind Enter para iniciar sesión
        self.window.bind('<Return>', lambda e: self.iniciar_sesion())
    
    def configurar_tema(self):
        """Configura un tema moderno para el login"""
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
            'bg_secundario': '#f5f7fa',
            'accent': '#0078d4',
            'accent_hover': '#005a9e',
            'text_primary': '#212529',
            'text_secondary': '#6c757d'
        }
        
        # Configurar Botones
        style.configure('TButton', 
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       relief='flat',
                       background=colores['accent'],
                       foreground='#000000')
        style.map('TButton',
                 background=[('active', colores['accent_hover']),
                           ('pressed', colores['accent_hover'])],
                 foreground=[('active', '#000000'),
                           ('pressed', '#000000')])
        
        # Configurar Entries
        style.configure('TEntry',
                       fieldbackground=colores['bg_principal'],
                       borderwidth=2,
                       relief='solid',
                       padding=10,
                       font=('Segoe UI', 10))
        style.map('TEntry',
                 bordercolor=[('focus', colores['accent'])],
                 lightcolor=[('focus', colores['accent'])],
                 darkcolor=[('focus', colores['accent'])])
        
        # Configurar Labels
        style.configure('TLabel',
                       background=colores['bg_secundario'],
                       foreground=colores['text_primary'],
                       font=('Segoe UI', 9))
        
        # Configurar fondo de la ventana
        self.window.configure(bg='#f0f2f5')
    
    def verificar_admin_por_defecto(self):
        """Crea un administrador por defecto si no existe ninguno"""
        try:
            empleados = self.empleado_mgr.listar()
            tiene_admin = False
            
            for emp in empleados:
                try:
                    # sqlite3.Row se accede como diccionario pero sin .get()
                    rol = emp['Rol'] if 'Rol' in emp.keys() else None
                    usuario = emp['Usuario'] if 'Usuario' in emp.keys() else None
                    if rol == 'admin' and usuario:
                        tiene_admin = True
                        break
                except:
                    continue
            
            if not tiene_admin:
                # Crear admin por defecto
                try:
                    self.empleado_mgr.crear(
                        nombre="Administrador",
                        cargo="Administrador del Sistema",
                        usuario="admin",
                        contrasena="admin123",
                        rol="admin"
                    )
                except Exception:
                    pass  # Si ya existe, no hacer nada
        except Exception:
            # Si hay error, intentar crear admin de todas formas
            try:
                self.empleado_mgr.crear(
                    nombre="Administrador",
                    cargo="Administrador del Sistema",
                    usuario="admin",
                    contrasena="admin123",
                    rol="admin"
                )
            except:
                pass
    
    def crear_interfaz(self):
        # Frame principal con fondo degradado
        main_frame = tk.Frame(self.window, bg='#f0f2f5')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame contenedor centrado con ancho fijo
        container = tk.Frame(main_frame, bg='#f0f2f5')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal con icono
        title_frame = tk.Frame(container, bg='#f0f2f5')
        title_frame.pack(pady=(0, 10))
        
        title_label = tk.Label(title_frame, 
                              text="💪 Mi propio esfuerzo", 
                              font=("Segoe UI", 42, "bold"),
                              bg='#f0f2f5',
                              fg='#0078d4')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, 
                                 text="Gestión Integral de Ventas", 
                                 font=("Segoe UI", 14),
                                 bg='#f0f2f5',
                                 fg='#6c757d')
        subtitle_label.pack(pady=(5, 0))
        
        # Separador
        separator = tk.Frame(container, bg='#dee2e6', height=1)
        separator.pack(fill=tk.X, pady=30, padx=100)
        
        # Frame de formulario con fondo blanco y sombra visual
        form_container = tk.Frame(container, bg='#e9ecef', relief='flat')
        form_container.pack(padx=20, pady=10)
        
        form_frame = tk.Frame(form_container, bg='#ffffff', relief='flat', bd=0)
        form_frame.pack(padx=3, pady=3)
        
        # Título del formulario
        form_title = tk.Label(form_frame, 
                             text="Iniciar Sesión", 
                             font=("Segoe UI", 18, "bold"),
                             bg='#ffffff',
                             fg='#000000')
        form_title.pack(pady=(30, 25))
        
        # Frame para campos de entrada
        fields_frame = tk.Frame(form_frame, bg='#ffffff')
        fields_frame.pack(fill=tk.X, padx=40, pady=10)
        
        # Usuario
        usuario_container = tk.Frame(fields_frame, bg='#ffffff')
        usuario_container.pack(fill=tk.X, pady=(0, 20))
        
        usuario_label = tk.Label(usuario_container, 
                               text="👤 Usuario", 
                               font=("Segoe UI", 11, "bold"),
                               bg='#ffffff',
                               fg='#495057',
                               anchor='w')
        usuario_label.pack(fill=tk.X, pady=(0, 8))
        
        self.entry_usuario = ttk.Entry(usuario_container, 
                                       width=35, 
                                       font=("Segoe UI", 11))
        self.entry_usuario.pack(fill=tk.X, ipady=10)
        
        # Contraseña
        contrasena_container = tk.Frame(fields_frame, bg='#ffffff')
        contrasena_container.pack(fill=tk.X, pady=(0, 25))
        
        contrasena_label = tk.Label(contrasena_container, 
                                   text="🔒 Contraseña", 
                                   font=("Segoe UI", 11, "bold"),
                                   bg='#ffffff',
                                   fg='#495057',
                                   anchor='w')
        contrasena_label.pack(fill=tk.X, pady=(0, 8))
        
        self.entry_contrasena = ttk.Entry(contrasena_container, 
                                         width=35, 
                                         show="●", 
                                         font=("Segoe UI", 11))
        self.entry_contrasena.pack(fill=tk.X, ipady=10)
        
        # Botón de login
        btn_frame = tk.Frame(form_frame, bg='#ffffff')
        btn_frame.pack(pady=(0, 30))
        
        login_btn = ttk.Button(btn_frame, 
                              text="🚀 Iniciar Sesión", 
                              command=self.iniciar_sesion,
                              width=32)
        login_btn.pack()
        
        # Información de ayuda
        help_frame = tk.Frame(form_frame, bg='#ffffff')
        help_frame.pack(pady=(0, 30))
        
        info_label = tk.Label(help_frame, 
                             text="💡 Credenciales por defecto:", 
                             font=("Segoe UI", 9),
                             bg='#ffffff',
                             fg='#6c757d')
        info_label.pack()
        
        credenciales_label = tk.Label(help_frame, 
                                     text="Usuario: admin  |  Contraseña: admin123", 
                                     font=("Segoe UI", 9, "bold"),
                                     bg='#ffffff',
                                     fg='#0078d4')
        credenciales_label.pack(pady=(5, 0))
        
        # Botón para salir - mejorado
        exit_btn = tk.Button(main_frame,
                           text="✕",
                           font=("Segoe UI", 18, "bold"),
                           bg='#dc3545',
                           fg='#ffffff',
                           activebackground='#c82333',
                           activeforeground='#ffffff',
                           borderwidth=0,
                           relief='flat',
                           width=3,
                           height=1,
                           command=self.window.quit,
                           cursor='hand2')
        exit_btn.place(relx=1.0, rely=0.0, anchor='ne', x=-15, y=15)
        
        # Agregar hover effect al botón de salida
        def on_enter(e):
            exit_btn.config(bg='#c82333')
        def on_leave(e):
            exit_btn.config(bg='#dc3545')
        exit_btn.bind("<Enter>", on_enter)
        exit_btn.bind("<Leave>", on_leave)
        
        # Crédito escondido - tooltip en el título
        def mostrar_credito(e):
            # Crédito escondido
            import tkinter.messagebox as msg
            msg.showinfo("", "helped with Purpura Development")
        title_label.bind("<Double-Button-1>", mostrar_credito)
    
    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get()
        
        if not usuario or not contrasena:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña")
            return
        
        empleado = self.empleado_mgr.autenticar(usuario, contrasena)
        
        if empleado:
            self.empleado_logueado = empleado
            # Restaurar decoraciones y salir de pantalla completa
            self.window.attributes('-fullscreen', False)
            self.window.overrideredirect(False)
            # Limpiar la ventana de login
            for widget in self.window.winfo_children():
                widget.destroy()
            # Ajustar tamaño de ventana para la GUI principal
            self.window.geometry("1200x700")
            # Centrar ventana
            self.window.update_idletasks()
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            x = (screen_width // 2) - (1200 // 2)
            y = (screen_height // 2) - (700 // 2)
            self.window.geometry(f"1200x700+{x}+{y}")
            self.callback(empleado)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.entry_contrasena.delete(0, tk.END)
            self.entry_usuario.focus()

