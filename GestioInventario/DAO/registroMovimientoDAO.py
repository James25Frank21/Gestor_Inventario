import mysql.connector
from dataBaseConexion import conectar


def guardar_movimiento(nombre_producto, descripcion_producto, categoria_producto, precio_producto, stock_minimo_producto, stock_maximo_producto, fecha_movimiento, tipo_movimiento, cantidad, proveedor_id, remitente):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO RegistroMovimientos (NombreProducto, DescripcionProducto, CategoriaProducto, PrecioProducto, StockMinimoProducto, StockMaximoProducto, FechaMovimiento, TipoMovimiento, Cantidad, ProveedorID, Remitente) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nombre_producto, descripcion_producto, categoria_producto, precio_producto, stock_minimo_producto, stock_maximo_producto, fecha_movimiento, tipo_movimiento, cantidad, proveedor_id, remitente)
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Movimiento guardado correctamente.")
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


def actualizar_movimiento(movimiento_id, nombre_producto, descripcion_producto, categoria_producto, precio_producto, stock_minimo_producto, stock_maximo_producto, fecha_movimiento, tipo_movimiento, cantidad, proveedor_id, remitente):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        if tipo_movimiento == "Salida":
            sql = "UPDATE RegistroMovimientos SET NombreProducto = %s, DescripcionProducto = %s, CategoriaProducto = %s, PrecioProducto = %s, StockMinimoProducto = %s, StockMaximoProducto = %s, TipoMovimiento = %s, Cantidad = %s, ProveedorID = NULL, Remitente = %s WHERE MovimientoID = %s"
            valores = (nombre_producto, descripcion_producto, categoria_producto, precio_producto, stock_minimo_producto, stock_maximo_producto, tipo_movimiento, cantidad, remitente, movimiento_id)
        else:
            sql = "UPDATE RegistroMovimientos SET NombreProducto = %s, DescripcionProducto = %s, CategoriaProducto = %s, PrecioProducto = %s, StockMinimoProducto = %s, StockMaximoProducto = %s,  TipoMovimiento = %s, Cantidad = %s, ProveedorID = %s, Remitente = %s WHERE MovimientoID = %s"
            valores = (nombre_producto, descripcion_producto, categoria_producto, precio_producto, stock_minimo_producto, stock_maximo_producto,  tipo_movimiento, cantidad, proveedor_id, remitente, movimiento_id)

        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Movimiento actualizado correctamente.")
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
