import sqlite3
from typing import Optional

class Database:
    """Clase para manejar la conexión a la base de datos"""
    
    def __init__(self, db_name: str = "sistema_ventas.db"):
        self.db_name = db_name
        self.connection: Optional[sqlite3.Connection] = None
        
    def connect(self):
        """Establece conexión con la base de datos"""
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            
    def execute_script(self, script_path: str):
        """Ejecuta un script SQL desde un archivo"""
        with open(script_path, 'r', encoding='utf-8') as file:
            script = file.read()
        
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executescript(script)
        conn.commit()
        self.disconnect()
        
    def execute_query(self, query: str, params: tuple = ()):
        """Ejecuta una consulta SQL"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        self.disconnect()
        return last_id
    
    def fetch_all(self, query: str, params: tuple = ()):
        """Obtiene todos los resultados de una consulta"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        self.disconnect()
        return results
    
    def fetch_one(self, query: str, params: tuple = ()):
        """Obtiene un solo resultado de una consulta"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        self.disconnect()
        return result
