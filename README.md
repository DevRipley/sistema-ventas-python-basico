# Sistema de Ventas en Python

## Ejecución local

1. Abra una terminal en la carpeta raíz del proyecto.
2. Active el entorno virtual si ya existe:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Instale dependencias si es necesario:

   ```powershell
   pip install fpdf2
   ```

4. Ejecute la aplicación:

   ```powershell
   python .\scripts\main.py
   ```

5. Inicie sesión con las credenciales por defecto si no hay administradores creados:

   - Usuario: `admin`
   - Contraseña: `admin123`

## Generar manual de usuario

Para crear o regenerar el manual de usuario en PDF, ejecute:

```powershell
python .\scripts\generar_manual_usuario.py
```

El archivo generado se guardará como `Manual_de_Usuario_Sistema_Ventas.pdf` en la carpeta raíz del proyecto.
