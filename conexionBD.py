import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="bd_carniceriasg",
    )
    cursor = conexion.cursor(buffered=True)
except Exception as e:
    print("...¡Por el momento no es posible conectarse con la BD, intentelo mas tarde!...", e)
