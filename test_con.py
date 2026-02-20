import oracledb
import sys
import os

# --- CONFIGURACIÓN DE TUS CREDENCIALES ---
# Cambia esto por tus datos reales
DB_USER = "USER_REPORT4"
DB_PASS = "aK251#57"
DB_DSN = oracledb.makedsn("172.16.0.178", 1521, sid="planos")

# --- CONFIGURACIÓN DEL INSTANT CLIENT ---
# CLIENT_DIR = r"/usr/lib/oracle/19.29/client64/lib"


def probar_conexion(usar_thick_mode=False):
    print("-" * 60)
    print(f"PRUEBA DE CONEXIÓN - MODO: {'THICK (Con Instant Client)' if usar_thick_mode else 'THIN (Python Puro)'}")
    print("-" * 60)

    conn = None
    try:
        # 1. Inicialización del Cliente (Solo para Thick Mode)
        if usar_thick_mode:
            try:
                # Verificamos si ya se inicializó antes para evitar errores al re-ejecutar
                if not oracledb.is_thin_mode():
                    print("ℹEl cliente ya estaba inicializado.")
                else:
                    #print(f"Cargando librerías desde: {CLIENT_DIR}")
                    #oracledb.init_oracle_client(lib_dir=CLIENT_DIR)
                    oracledb.init_oracle_client(lib_dir=None)
            except Exception as e:
                print("\nFALLÓ LA CARGA DE LIBRERÍAS (DPI-1047 o similar):")
                print(f" {e}")
                print(
                    "\nSUGERENCIA: Revisa 'libaio1', el enlace simbólico 'libclntsh.so' o la arquitectura (32/64 bits).")
                return  # Detenemos aquí si falla la librería

        # 2. Intento de Conexión
        print(f"Conectando a {DB_DSN} como {DB_USER}...")

        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASS,
            dsn=DB_DSN
        )

        # 3. Verificación de Datos (Query real)
        cursor = conn.cursor()

        # Obtenemos versión de la BD para confirmar
        cursor.execute("SELECT banner FROM v$version WHERE ROWNUM = 1")
        version_bd = cursor.fetchone()[0]

        print(" ¡CONEXIÓN EXITOSA!")
        print(f"Versión Cliente Python: {oracledb.version}")
        print(f"Modo actual: {'Thick' if not conn.thin else 'Thin'}")
        print(f"Base de Datos: {version_bd}")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f" ERROR DE BASE DE DATOS:")
        print(f" Código: {error.code}")
        print(f" Mensaje: {error.message}")

        if error.code == 1017:
            print("   (Usuario o contraseña incorrectos)")
        elif error.code == 12154:
            print("   (No se puede resolver el nombre del servicio/DSN)")
        elif error.code == 12541:
            print("   (No hay nadie escuchando en ese host/puerto)")

    except Exception as ex:
        print(f" ERROR GENERAL:\n   {ex}")

    finally:
        if conn:
            conn.close()
            print("Conexión cerrada correctamente.")


if __name__ == "__main__":
    # --- PRUEBA 1: MODO THIN (Recomendado, no requiere instalación) ---
    print("\n>>> EJECUTANDO PRUEBA 1: MODO THIN (Sin dependencias)")
    probar_conexion(usar_thick_mode=False)

    print("\n" + "=" * 60 + "\n")

    # --- PRUEBA 2: MODO THICK (El que te estaba fallando) ---
    # Cambia a True si quieres intentar depurar tu instalación de Oracle Client
    EJECUTAR_THICK = True

    if EJECUTAR_THICK:
        print(">>> EJECUTANDO PRUEBA 2: MODO THICK (Usando /opt/oracle...)")
        probar_conexion(usar_thick_mode=True)
    else:
        print(">>> SALTANDO PRUEBA 2 (Modo Thick desactivado en el código)")
