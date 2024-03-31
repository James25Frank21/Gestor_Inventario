class RegistroMovimiento:
    def __init__(self, movimiento_id, nombre_producto, descripcion_producto, categoria_producto, precio_producto,stock_minimo_producto, stock_maximo_producto, fecha_movimiento, tipo_movimiento, cantidad, proveedor_id, remitente):

        self.movimiento_id = movimiento_id
        self.nombre_producto = nombre_producto
        self.descripcion_producto = descripcion_producto
        self.categoria_producto = categoria_producto
        self.precio_producto = precio_producto
        self.stock_minimo_producto = stock_minimo_producto
        self.stock_maximo_producto = stock_maximo_producto
        self.fecha_movimiento = fecha_movimiento
        self.tipo_movimiento = tipo_movimiento
        self.cantidad = cantidad
        self.proveedor_id = proveedor_id
        self.remitente = remitente
