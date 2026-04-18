# Sales system in Python

*Automatically synced with your [v0.app](https://v0.app) deployments*

[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com/luisdestrellas-projects/v0-sales-system-in-python)
[![Built with v0](https://img.shields.io/badge/Built%20with-v0.app-black?style=for-the-badge)](https://v0.app/chat/kWIFyiN9XZa)

## Overview

This repository will stay in sync with your deployed chats on [v0.app](https://v0.app).
Any changes you make to your deployed app will be automatically pushed to this repository from [v0.app](https://v0.app).

## Deployment

Your project is live at:

**[https://vercel.com/luisdestrellas-projects/v0-sales-system-in-python](https://vercel.com/luisdestrellas-projects/v0-sales-system-in-python)**

## Build your app

Continue building your app on:

**[https://v0.app/chat/kWIFyiN9XZa](https://v0.app/chat/kWIFyiN9XZa)**

## How It Works

1. Create and modify your project using [v0.app](https://v0.app)
2. Deploy your chats from the v0 interface
3. Changes are automatically pushed to this repository
4. Vercel deploys the latest version from this repository

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
