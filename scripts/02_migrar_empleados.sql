-- Script de migración para agregar campos de usuario y contraseña a empleados existentes
-- Este script se ejecuta solo si los campos no existen

-- Agregar columnas si no existen
-- SQLite no soporta ALTER TABLE ADD COLUMN IF NOT EXISTS directamente
-- Por lo tanto, usamos un enfoque con manejo de errores en Python

