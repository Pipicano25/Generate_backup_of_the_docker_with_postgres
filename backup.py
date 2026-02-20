import subprocess
import sys
from pathlib import Path
import re

# ========= CONFIGURACIÓN =========
CONTAINER_NAME = "postgres17"
DB_USER = "postgre"
BACKUP_DIR = Path(".")  # carpeta donde están los .sqlc
# =================================

def run(cmd, input_file=None):
    print(f"\n▶ Ejecutando: {' '.join(cmd)}")
    try:
        if input_file:
            with open(input_file, "rb") as f:
                subprocess.run(cmd, stdin=f, check=True)
        else:
            subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando comando")
        sys.exit(1)

def db_name_from_file(file: Path) -> str:
    """
    Convierte:
    asdata_bd_2025-12-23_10-12-46.sqlc
    → asdata_bd
    """
    name = file.stem
    name = re.sub(r"_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$", "", name)
    return name


def restore():

    option = input("¿Desea restaurar las bases de datos? (s/n): ")
    if option.lower() != "s": return False

    sqlc_files = sorted(BACKUP_DIR.glob("*.sqlc"))
    print(sqlc_files)

    if not sqlc_files:
        print("❌ No se encontraron archivos .sqlc")
        sys.exit(1)

    for backup in sqlc_files:
        db_name = db_name_from_file(backup)

        print("\n" + "=" * 60)
        print(f"📦 Restaurando backup: {backup.name}")
        print(f"🗄️  Base de datos: {db_name}")
        print("=" * 60)

        # 1️⃣ Cerrar conexiones
        run([
            "docker", "exec", "-i", CONTAINER_NAME,
            "psql", "-U", DB_USER, "-d", "postgres",
            "-c", f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{db_name}';
            """
        ])

        # 2️⃣ Eliminar DB
        run([
            "docker", "exec", "-i", CONTAINER_NAME,
            "psql", "-U", DB_USER, "-d", "postgres",
            "-c", f"DROP DATABASE IF EXISTS {db_name};"
        ])
        
        # 3️⃣ Crear DB
        print("\n3️⃣ Creando base de datos")
        run([
            "docker", "exec", "-i", CONTAINER_NAME,
            "psql", "-U", DB_USER, "-d", "postgres",
            "-c", f"CREATE DATABASE {db_name};"
        ])

        # 4️⃣ Restaurar
        print("\n4️⃣ Restaurando base de datos")
        run([
            "docker", "exec", "-i", CONTAINER_NAME,
            "pg_restore",
            "--no-owner",
            "--no-privileges",
            "-U", DB_USER,
            "-d", db_name
        ], input_file=backup)

    print("\n✅ Todas las bases fueron restauradas correctamente")


def main():
    general_option = input("Que opcion deseas realizar?: \n1. Restaurar \n2. Backup \n3. Salir (presiona cualquier tecla)")

    if general_option == "1":
        restore()
    elif general_option == "2":
        backup()
    else:
        print("Opcion no valida")

if __name__ == "__main__":
    main()
