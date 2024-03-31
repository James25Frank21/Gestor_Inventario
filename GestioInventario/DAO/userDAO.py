import mysql.connector
from dataBaseConexion import conectar

def guardar_usuario(nombre_usuario, contraseña, rol):

    try:
        conexion = conectar()
        with conexion.cursor() as cursor:
            sql = "INSERT INTO Usuarios (NombreUsuario, Contraseña, Rol) VALUES (%s, %s, %s)"
            valores = (nombre_usuario, contraseña, rol)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
        print("Usuario guardado correctamente.")
    except mysql.connector.Error as error:
        print("Error al guardar el usuario:", error)

def obtener_usuarios():
    try:
        conexion = conectar()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM Usuarios")
            usuarios = cursor.fetchall()
            cursor.close()
            conexion.close()
        return usuarios

    except mysql.connector.Error as error:
        print("Error al obtener los usuarios:", error)
        return []

def eliminar_usuario(usuario_id):
    try:
        conexion = conectar()
        with conexion.cursor() as cursor:
            sql = "DELETE FROM Usuarios WHERE UsuarioID = %s"
            cursor.execute(sql, (usuario_id,))
            conexion.commit()
            cursor.close()
            conexion.close()
        print("Usuario eliminado correctamente.")
    except mysql.connector.Error as error:
        print("Error al eliminar el usuario:", error)

def actualizar_usuario(usuario_id, nombre_usuario, contraseña, rol):
    try:
        conexion = conectar()
        with conexion.cursor() as cursor:
            sql = "UPDATE Usuarios SET NombreUsuario = %s, Contraseña = %s, Rol = %s WHERE UsuarioID = %s"
            valores = (nombre_usuario, contraseña, rol, usuario_id)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
        print("Usuario actualizado correctamente.")
    except mysql.connector.Error as error:
        print("Error al actualizar el usuario:", error)
