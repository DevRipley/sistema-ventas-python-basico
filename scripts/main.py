import tkinter as tk
from database import Database
import os

def inicializar_base_datos():
    """Inicializa la base de datos ejecutando el script SQL"""
    try:
        db = Database()
        script_path = os.path.join(os.path.dirname(__file__), "01_crear_base_datos.sql")
        
        # Verificar si las tablas ya existen
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Cliente'")
        existe = cursor.fetchone()
        
        if not existe:
            db.disconnect()
            db.execute_script(script_path)
        else:
            # Migrar tabla Empleado si es necesario (agregar campos Usuario, Contrasena y Rol)
            try:
                cursor.execute("SELECT Usuario FROM Empleado LIMIT 1")
            except:
                # Los campos no existen, agregarlos
                try:
                    # Agregar columnas sin restricción UNIQUE (SQLite no permite UNIQUE en ALTER TABLE)
                    cursor.execute("ALTER TABLE Empleado ADD COLUMN Usuario TEXT")
                    cursor.execute("ALTER TABLE Empleado ADD COLUMN Contrasena TEXT")
                    cursor.execute("ALTER TABLE Empleado ADD COLUMN Rol TEXT DEFAULT 'empleado'")
                    
                    # Crear índice único solo para valores no NULL
                    try:
                        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_empleado_usuario ON Empleado(Usuario) WHERE Usuario IS NOT NULL")
                    except:
                        pass
                    
                    conn.commit()
                except Exception as e:
                    print(f"Error al migrar tabla Empleado: {e}")
            else:
                # Verificar si existe el campo Rol
                try:
                    cursor.execute("SELECT Rol FROM Empleado LIMIT 1")
                except:
                    try:
                        cursor.execute("ALTER TABLE Empleado ADD COLUMN Rol TEXT DEFAULT 'empleado'")
                        conn.commit()
                    except Exception as e:
                        print(f"Error al agregar campo Rol: {e}")
            db.disconnect()
    except Exception as e:
        # Si hay error, crear las tablas
        try:
            db.disconnect()
        except:
            pass
        try:
            db.execute_script(script_path)
        except Exception as e2:
            print(f"Error crítico al inicializar base de datos: {e2}")

def main():
    """Función principal del sistema - Inicia la interfaz gráfica"""
    # Inicializar base de datos
    inicializar_base_datos()
    
    # Crear ventana raíz
    root = tk.Tk()
    
    # Mostrar login
    from login import LoginWindow
    from gui import SistemaVentasGUI
    
    def on_login_success(empleado):
        """Callback cuando el login es exitoso"""
        app = SistemaVentasGUI(root, empleado)
    
    login = LoginWindow(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()
