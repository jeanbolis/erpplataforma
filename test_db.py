## --- Smoke test de conexão

from erp.db import get_connection

with get_connection() as conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT 1 AS ok")
    print("Conexão OK:", cursor.fetchall())
