from app.core.database import engine

try:
    conn = engine.connect()
    print("SQL Server Connected Successfully")
    conn.close()

except Exception as ex:
    print(ex)