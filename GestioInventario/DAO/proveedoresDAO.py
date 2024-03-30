import mysql.connector
from dataBaseConexion import conectar


def guardar_proveedor(nombre,apellido, direccion, telefono, email):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO Proveedores (Nombre,Apellido, Direccion, Telefono, Email) VALUES (%s,%s, %s, %s, %s)"
        valores = (nombre,apellido, direccion, telefono, email)
        cursor.execute(sql, valores)

        conexion.commit()

        cursor.close()
        conexion.close()

        print("Proveedor guardado correctamente.")

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

def obtener_proveedores():
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM Proveedores")
        proveedores = cursor.fetchall()

        cursor.close()
        conexion.close()

        return proveedores

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

def eliminar_proveedor(proveedor_id):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = "DELETE FROM Proveedores WHERE ProveedorID = %s"
        cursor.execute(sql, (proveedor_id,))

        conexion.commit()

        cursor.close()
        conexion.close()

        print("Proveedor eliminado correctamente.")

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

def actualizar_proveedor(proveedor_id, nombre,apellido, direccion, telefono, email):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = "UPDATE Proveedores SET Nombre = %s,Apellido = %s, Direccion = %s, Telefono = %s, Email = %s WHERE ProveedorID = %s"
        valores = (nombre, direccion, telefono, email, proveedor_id)
        cursor.execute(sql, valores)

        conexion.commit()

        cursor.close()
        conexion.close()

        print("Proveedor actualizado correctamente.")

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

