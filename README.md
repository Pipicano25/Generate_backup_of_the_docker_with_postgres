# Generate_backup_of_the_docker_with_postgres

Herramientas para gestionar bases de datos desde un contenedor Docker: restaura bases de datos PostgreSQL a partir de archivos de respaldo `.sqlc` (mediante `docker exec` + `psql`/`pg_restore`) e incluye un script independiente para probar la conexión a una base de datos Oracle con `oracledb`.

## Tecnologías

- Python 3
- PostgreSQL 17 (contenedor Docker)
- Docker
- Oracle (`oracledb`)
- `psql` / `pg_restore`

## Scripts

| Archivo | Descripción |
|---|---|
| `backup.py` | Restaura bases PostgreSQL desde archivos `.sqlc` usando `docker exec` |
| `test_con.py` | Prueba de conexión a Oracle en modo Thin y Thick |
| `requirements.txt` | Dependencias (`oracledb`, `cryptography`, `cffi`, etc.) |

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

Edita las variables de configuración al inicio de cada script (`CONTAINER_NAME`, `DB_USER`, credenciales de Oracle) y ejecuta:

```bash
python backup.py
python test_con.py
```

## Licencia

MIT
