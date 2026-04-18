import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / '.venv'
PYTHON = sys.executable

REQUIRED_PACKAGES = [
    'fpdf2'
]


def run_command(cmd, cwd=None, env=None):
    print('Ejecutando:', ' '.join(str(c) for c in cmd))
    result = subprocess.run(cmd, cwd=cwd, shell=False, env=env)
    if result.returncode != 0:
        raise SystemExit(f'Comando falló con código {result.returncode}')


def create_virtualenv():
    if VENV_DIR.exists():
        print('Entorno virtual existente:', VENV_DIR)
        return

    print('Creando entorno virtual en', VENV_DIR)
    run_command([PYTHON, '-m', 'venv', str(VENV_DIR)], cwd=ROOT)
    print('Entorno virtual creado.')


def get_venv_python():
    if os.name == 'nt':
        return VENV_DIR / 'Scripts' / 'python.exe'
    return VENV_DIR / 'bin' / 'python'


def install_dependencies(python_executable):
    print('Instalando dependencias...')
    run_command([str(python_executable), '-m', 'pip', 'install', '--upgrade', 'pip'], cwd=ROOT)
    run_command([str(python_executable), '-m', 'pip', 'install', *REQUIRED_PACKAGES], cwd=ROOT)
    print('Dependencias instaladas.')


def run_application(python_executable):
    main_script = ROOT / 'scripts' / 'main.py'
    if not main_script.exists():
        raise SystemExit('No se encontró el archivo de entrada: scripts/main.py')

    print('Iniciando aplicación...')
    run_command([str(python_executable), str(main_script)], cwd=ROOT)
    print('La aplicación ha finalizado.')


def main():
    os.chdir(ROOT)

    create_virtualenv()
    python_exec = get_venv_python()
    if not python_exec.exists():
        raise SystemExit(f'No se encontró el intérprete en el entorno virtual: {python_exec}')

    install_dependencies(python_exec)
    run_application(python_exec)


if __name__ == '__main__':
    main()
