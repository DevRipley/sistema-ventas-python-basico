-- Crear base de datos del sistema de ventas

-- Tabla de Clientes
CREATE TABLE IF NOT EXISTS Cliente (
    ID_Cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Telefono TEXT,
    Direccion TEXT
);

-- Tabla de Proveedores
CREATE TABLE IF NOT EXISTS Proveedor (
    ID_Proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Telefono TEXT,
    Direccion TEXT
);

-- Tabla de Productos
CREATE TABLE IF NOT EXISTS Producto (
    ID_Producto INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Categoria TEXT,
    Precio REAL NOT NULL CHECK(Precio >= 0),
    Stock INTEGER NOT NULL DEFAULT 0 CHECK(Stock >= 0),
    Proveedor_ID INTEGER,
    FOREIGN KEY (Proveedor_ID) REFERENCES Proveedor(ID_Proveedor)
);

-- Tabla de Empleados
CREATE TABLE IF NOT EXISTS Empleado (
    ID_Empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Cargo TEXT
);

-- Tabla de Ventas
CREATE TABLE IF NOT EXISTS Venta (
    ID_Venta INTEGER PRIMARY KEY AUTOINCREMENT,
    Fecha TEXT NOT NULL,
    ID_Cliente INTEGER NOT NULL,
    ID_Empleado INTEGER NOT NULL,
    FOREIGN KEY (ID_Cliente) REFERENCES Cliente(ID_Cliente),
    FOREIGN KEY (ID_Empleado) REFERENCES Empleado(ID_Empleado)
);

-- Tabla de Detalle de Venta
CREATE TABLE IF NOT EXISTS Detalle_Venta (
    ID_Detalle INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Venta INTEGER NOT NULL,
    ID_Producto INTEGER NOT NULL,
    Cantidad INTEGER NOT NULL CHECK(Cantidad > 0),
    Precio_Unitario REAL NOT NULL CHECK(Precio_Unitario >= 0),
    FOREIGN KEY (ID_Venta) REFERENCES Venta(ID_Venta),
    FOREIGN KEY (ID_Producto) REFERENCES Producto(ID_Producto)
);
