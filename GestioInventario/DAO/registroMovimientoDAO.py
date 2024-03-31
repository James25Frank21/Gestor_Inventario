import mysql.connector
from dataBaseConexion import conectar
from model.registroMovimiento import RegistroMovimiento


class RegistroMovimientoDAO:
    @staticmethod
    def guardar_movimiento(movimiento):
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                sql = "INSERT INTO registromovimientos (NombreProducto, DescripcionProducto, CategoriaProducto, PrecioProducto, StockMinimoProducto, StockMaximoProducto, FechaMovimiento, TipoMovimiento, Cantidad, ProveedorID, Remitente) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                valores = (movimiento.nombre_producto, movimiento.descripcion_producto, movimiento.categoria_producto, movimiento.precio_producto, movimiento.stock_minimo_producto, movimiento.stock_maximo_producto, movimiento.fecha_movimiento, movimiento.tipo_movimiento, movimiento.cantidad, movimiento.proveedor_id, movimiento.remitente)
                cursor.execute(sql, valores)
                conexion.commit()
                cursor.close()
                conexion.close()
            print("Movimiento guardado correctamente.")
        except mysql.connector.Error as error:
            print("Error al guardar el movimiento:", error)

    @staticmethod
    def actualizar_movimiento(movimiento):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            if movimiento.tipo_movimiento == "Salida":
                sql = "UPDATE RegistroMovimientos SET NombreProducto = %s, DescripcionProducto = %s, CategoriaProducto = %s, PrecioProducto = %s, StockMinimoProducto = %s, StockMaximoProducto = %s, TipoMovimiento = %s, Cantidad = %s, ProveedorID = NULL, Remitente = %s WHERE MovimientoID = %s"
                valores = (
                movimiento.nombre_producto, movimiento.descripcion_producto, movimiento.categoria_producto, movimiento.precio_producto, movimiento.stock_minimo_producto,
                movimiento.stock_maximo_producto, movimiento.tipo_movimiento, movimiento.cantidad, movimiento.remitente, movimiento.movimiento_id)
            else:
                sql = "UPDATE RegistroMovimientos SET NombreProducto = %s, DescripcionProducto = %s, CategoriaProducto = %s, PrecioProducto = %s, StockMinimoProducto = %s, StockMaximoProducto = %s,  TipoMovimiento = %s, Cantidad = %s, ProveedorID = %s, Remitente = %s WHERE MovimientoID = %s"
                valores = (
                movimiento.nombre_producto, movimiento.descripcion_producto, movimiento.categoria_producto, movimiento.precio_producto, movimiento.stock_minimo_producto,
                movimiento.stock_maximo_producto, movimiento.tipo_movimiento, movimiento.cantidad, movimiento.proveedor_id, movimiento.remitente, movimiento.movimiento_id)

            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            print("Movimiento actualizado correctamente.")
        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos:", error)

    @staticmethod
    def obtener_movimientos():
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM RegistroMovimientos")
                usuarios = []
                for usuario_data in cursor.fetchall():
                    usuario = RegistroMovimiento(*usuario_data)
                    usuarios.append(usuario)
            return usuarios
        except mysql.connector.Error as error:
            print("Error al obtener los usuarios:", error)
            return []

    @staticmethod
    def eliminar_movimiento(movimiento_id):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "DELETE FROM RegistroMovimientos WHERE MovimientoID = %s"
            cursor.execute(sql, (movimiento_id,))
            conexion.commit()
            cursor.close()
            conexion.close()
            print("Movimiento eliminado correctamente.")
        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos:", error)
def obtener_movimientos():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM RegistroMovimientos")
        movimientos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return movimientos
    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

def obtener_fecha():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT CURDATE()")  # CURDATE() es una función de MySQL que devuelve la fecha de hoy
        fecha = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fecha
    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

def exportar_movimientos():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM RegistroMovimientos")
        movimientos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return movimientos
    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)
