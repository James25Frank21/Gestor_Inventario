import mysql.connector
from dataBaseConexion import conectar
from model.User import *

class UsuarioDAO:
    @staticmethod
    def guardar_usuario(usuario):
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                sql = "INSERT INTO Usuarios (NombreUsuario, Contraseña, Rol) VALUES (%s, %s, %s)"
                valores = (usuario.nombre_usuario, usuario.contraseña, usuario.rol)
                cursor.execute(sql, valores)
                conexion.commit()
                cursor.close()
                conexion.close()
            print("Usuario guardado correctamente.")
        except mysql.connector.Error as error:
            print("Error al guardar el usuario:", error)

    @staticmethod
    def obtener_usuarios():
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM Usuarios")
                usuarios = []
                for usuario_data in cursor.fetchall():
                    usuario = Usuario(*usuario_data)
                    usuarios.append(usuario)
            return usuarios
        except mysql.connector.Error as error:
            print("Error al obtener los usuarios:", error)
            return []

    @staticmethod
    def eliminar_usuario(usuario_id):
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                sql = "DELETE FROM Usuarios WHERE UsuarioID = %s"
                cursor.execute(sql, (usuario_id,))
                conexion.commit()
            print("Usuario eliminado correctamente.")
        except mysql.connector.Error as error:
            print("Error al eliminar el usuario:", error)

    @staticmethod
    def actualizar_usuario(usuario):
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                sql = "UPDATE Usuarios SET NombreUsuario = %s, Contraseña = %s, Rol = %s WHERE UsuarioID = %s"
                valores = (usuario.nombre_usuario, usuario.contraseña, usuario.rol, usuario.usuario_id)
                cursor.execute(sql, valores)
                conexion.commit()
            print("Usuario actualizado correctamente.")
        except mysql.connector.Error as error:
            print("Error al actualizar el usuario:", error)

    @staticmethod
    def login(nombre_usuario, contraseña):
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM Usuarios WHERE NombreUsuario = %s AND Contraseña = %s"
                cursor.execute(sql, (nombre_usuario, contraseña))
                usuario_data = cursor.fetchone()
                if usuario_data:
                    return Usuario(*usuario_data)
                return None
        except mysql.connector.Error as error:
            print("Error al iniciar sesión:", error)
            return None
