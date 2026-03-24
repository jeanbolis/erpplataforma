### ---Pool + Context Manager (base de todo o ERP)

import mysql.connector
from mysql.connector import pooling
from erp.config import DBConfig

_pool = pooling.MySQLConnectionPool(
    pool_name=DBConfig.POOL_NAME,
    pool_size=DBConfig.POOL_SIZE,
    host=DBConfig.HOST,
    port=DBConfig.PORT,
    user=DBConfig.USER,
    password=DBConfig.PASSWORD,
    database=DBConfig.DATABASE,
    charset="utf8mb4",
    collation="utf8mb4_0900_ai_ci",
)

def get_connection():
    class ConnectionContext:
        def __enter__(self):
            self.conn = _pool.get_connection()
            self.conn.autocommit = False
            return self.conn

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

    return ConnectionContext()
