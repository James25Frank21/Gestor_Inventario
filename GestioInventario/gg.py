import mysql.connector
from dataBaseConexion import conectar

class Proveedor:
    def __init__(self, proveedor_id, nombre, apellido, direccion, telefono, email):
        self.proveedor_id = proveedor_id
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    @classmethod
    def from_database(cls, proveedor_id):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "SELECT * FROM Proveedores WHERE ProveedorID = %s"
            cursor.execute(sql, (proveedor_id,))
            proveedor_data = cursor.fetchone()
            if proveedor_data:
                proveedor = cls(*proveedor_data)
                return proveedor
            else:
                return None
        except mysql.connector.Error as error:
            print("Error al obtener el proveedor:", error)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def guardar_proveedor(self):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "INSERT INTO Proveedores (Nombre, Apellido, Direccion, Telefono, Email) VALUES (%s, %s, %s, %s, %s)"
            valores = (self.nombre, self.apellido, self.direccion, self.telefono, self.email)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Proveedor guardado correctamente.")
        except mysql.connector.Error as error:
            print("Error al guardar el proveedor:", error)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def eliminar_proveedor(self):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "DELETE FROM Proveedores WHERE ProveedorID = %s"
            cursor.execute(sql, (self.proveedor_id,))
            conexion.commit()
            print("Proveedor eliminado correctamente.")
        except mysql.connector.Error as error:
            print("Error al eliminar el proveedor:", error)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def actualizar_proveedor(self):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "UPDATE Proveedores SET Nombre = %s, Apellido = %s, Direccion = %s, Telefono = %s, Email = %s WHERE ProveedorID = %s"
            valores = (self.nombre, self.apellido, self.direccion, self.telefono, self.email, self.proveedor_id)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Proveedor actualizado correctamente.")
        except mysql.connector.Error as error:
            print("Error al actualizar el proveedor:", error)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    #select * from proveedores
    def obtener_proveedores(cls):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Proveedores")
            proveedores = cursor.fetchall()
            return proveedores
        except mysql.connector.Error as error:
            print("Error al obtener los proveedores:", error)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
