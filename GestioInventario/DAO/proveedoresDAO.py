import mysql.connector
from dataBaseConexion import conectar
from model.Proveedores import *

class ProveedorDAO:
    @staticmethod
    def insertar_proveedor(proveedor):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "INSERT INTO Proveedores (Nombre, Apellido, Direccion, Telefono, Email) VALUES (%s, %s, %s, %s, %s)"
            valores = (proveedor.nombre, proveedor.apellido, proveedor.direccion, proveedor.telefono, proveedor.email)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Proveedor insertado correctamente.")
        except mysql.connector.Error as error:
            print("Error al insertar el proveedor:", error)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_proveedor(proveedor):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "UPDATE Proveedores SET Nombre = %s, Apellido = %s, Direccion = %s, Telefono = %s, Email = %s WHERE ProveedorID = %s"
            valores = (proveedor.nombre, proveedor.apellido, proveedor.direccion, proveedor.telefono, proveedor.email, proveedor.proveedor_id)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Proveedor actualizado correctamente.")
        except mysql.connector.Error as error:
            print("Error al actualizar el proveedor:", error)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_proveedor(id_proveedor):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "DELETE FROM Proveedores WHERE ProveedorID = %s"
            cursor.execute(sql, (id_proveedor,))
            conexion.commit()
            print("Proveedor eliminado correctamente.")
        except mysql.connector.Error as error:
            print("Error al eliminar el proveedor:", error)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def obtener_proveedores():
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Proveedores")
            proveedores = []
            for proveedor_data in cursor.fetchall():
                proveedor = Proveedor(*proveedor_data)
                proveedores.append(proveedor)
            return proveedores
        except mysql.connector.Error as error:
            print("Error al obtener los proveedores:", error)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    #select * from proveedores
def obtener_proveedor():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Proveedores")
        proveedores = cursor.fetchall()
        return proveedores
    except mysql.connector.Error as error:
        print("Error al obtener los proveedores:", error)
