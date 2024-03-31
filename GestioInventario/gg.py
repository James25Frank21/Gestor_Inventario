import sys
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QFormLayout, QWidget, QHBoxLayout, QPushButton, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QFileDialog, QDialog
from PyQt6.QtGui import QPixmap, QIcon
from DAO.registroMovimientoDAO import obtener_movimientos, guardar_movimiento, actualizar_movimiento, \
    eliminar_movimiento, obtener_fecha
from DAO.proveedoresDAO import obtener_proveedores
from openpyxl import Workbook


class DialogoTabla(QDialog):
    celda_clickeada = pyqtSignal(int)

    def __init__(self, proveedores):
        super().__init__()
        self.setWindowTitle("Tabla de proveedores")
        layout = QVBoxLayout(self)
        #tamaño de la ventana
        self.setGeometry(350, 100, 630, 300)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ProveedorID", "Nombre", "Apellido", "Dirección", "Teléfono", "Email"])
        self.table.setRowCount(len(proveedores))
        for row, proveedor in enumerate(proveedores):
            for column, data in enumerate(proveedor):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))
        self.table.cellClicked.connect(self.on_cell_clicked)
        layout.addWidget(self.table)

    def on_cell_clicked(self, row, column):
        id_celda = int(self.table.item(row, 0).text())
        self.celda_clickeada.emit(id_celda)
        self.accept()



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Movimientos de Inventario")
        self.setWindowIcon(QIcon("img/pngegg (5).png"))
        self.setGeometry(350, 100, 630, 550)

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.registro_label = QLabel("Registro de  Inventario")
        self.form_layout.addRow(self.registro_label)

        self.NombreProducto_input = QLineEdit()
        self.form_layout.addRow(QLabel("NombreProducto:"), self.NombreProducto_input)
        self.DescripcionProducto_input = QLineEdit()
        self.form_layout.addRow(QLabel("DescripcionProducto:"), self.DescripcionProducto_input)

        self.CategoriaProducto_input = QComboBox()
        categorias = ["Alimentos", "Bebidas", "Limpieza", "Higiene", "Electrodomesticos", "Ropa", "Calzado",
                      "Accesorios", "Herramientas", "Juguetes", "Electronica", "Muebles", "Decoracion"]
        self.CategoriaProducto_input.addItems(categorias)
        self.form_layout.addRow(QLabel("CategoriaProducto:"), self.CategoriaProducto_input)

        self.PrecioProducto_input = QLineEdit()
        self.form_layout.addRow(QLabel("PrecioProducto:"), self.PrecioProducto_input)

        self.TipoMovimiento_input = QComboBox()
        tipos = ["Seleccione", "Ajuste", "Salida", "Entrada"]
        self.TipoMovimiento_input.addItems(tipos)
        self.TipoMovimiento_input.currentTextChanged.connect(self.actualizar_campos)
        self.form_layout.addRow(QLabel("TipoMovimiento:"), self.TipoMovimiento_input)

        self.Cantidad_input = QLineEdit()
        self.form_layout.addRow(QLabel("Cantidad:"), self.Cantidad_input)

        self.boton_abrir_dialogo = QPushButton("Ver Proveedores", self)
        self.boton_abrir_dialogo.setFixedSize(120, 23)
        self.boton_abrir_dialogo.clicked.connect(self.mostrar_dialogo)

        self.ProveedorID_input = QLineEdit(self)
        self.ProveedorID_input.setReadOnly(True)#para que no se pueda editar

        self.form_layout.addRow(self.boton_abrir_dialogo, self.ProveedorID_input)

        self.Remitente_input = QLineEdit()
        self.form_layout.addRow(QLabel("Remitente:"), self.Remitente_input)

        for i in range(self.form_layout.rowCount()):
            self.form_layout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().setFixedWidth(200)

        self.form_layout.addRow(QLabel(""))

        layout_vbox_buttons = QHBoxLayout()
        self.form_layout.addRow(layout_vbox_buttons)

        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")
        self.export_button = QPushButton("Exportar")
        self.limpiar_campo = QPushButton("Limpiar")

        self.add_button.clicked.connect(self.guardar_movimiento)
        self.update_button.clicked.connect(self.actualizar_movimiento)
        self.delete_button.clicked.connect(self.eliminar_movimiento)
        self.export_button.clicked.connect(self.exportar_movimiento)
        self.limpiar_campo.clicked.connect(self.limpiar_campos)

        layout_vbox_buttons.addWidget(self.add_button)
        layout_vbox_buttons.addWidget(self.update_button)
        layout_vbox_buttons.addWidget(self.delete_button)
        layout_vbox_buttons.addWidget(self.export_button)
        layout_vbox_buttons.addWidget(self.limpiar_campo)

        self.add_button.setFixedSize(80, 30)
        self.update_button.setFixedSize(80, 30)
        self.delete_button.setFixedSize(80, 30)
        self.export_button.setFixedSize(80, 30)
        self.limpiar_campo.setFixedSize(80, 30)

        layout_hbox = QHBoxLayout()
        layout_hbox.addLayout(self.form_layout)

        self.image_label = QLabel()
        pixmap = QPixmap("img/pngegg (2).png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(400, 350)

        layout_hbox.addWidget(self.image_label)

        layout_vbox = QVBoxLayout()
        layout_vbox.addLayout(layout_hbox)

        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(["movimiento_id", "nombre_producto", "descripcion_producto",
                                               "categoria_producto", "precio_producto", "stock_minimo_producto",
                                               "stock_maximo_producto", "fecha_movimiento", "tipo_movimiento",
                                               "cantidad", "proveedor_id", "remitente"])
        self.table.cellClicked.connect(self.seleccionar_movimiento)
        self.cargar_movimiento()

        layout_vbox.addWidget(self.table)
        self.setLayout(layout_vbox)

    def mostrar_dialogo(self):
        try:
            # Obtener los datos reales de la tabla de proveedores
            proveedores = obtener_proveedores()  # Suponiendo que obtener_proveedores() obtiene los datos de la tabla de proveedores

            # Crear una instancia de DialogoTabla con los datos de proveedores
            dialogo = DialogoTabla(proveedores)
            # Conectar la señal celda_clickeada a actualizar_id
            dialogo.celda_clickeada.connect(self.actualizar_id)
            # Mostrar el diálogo
            dialogo.exec()
        except Exception as e:
            print("Error al mostrar el diálogo:", e)

    def actualizar_id(self, id_celda):
        self.ProveedorID_input.setText(str(id_celda))
    def exportar_movimiento(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Exportar Movimientos", "", "Archivos XLSX (*.xlsx)")
        if file_path:
            try:
                wb = Workbook()
                ws_movimientos = wb.active
                ws_movimientos.title = "Movimientos"
                ws_movimientos.append(["ID Movimiento", "Nombre Producto", "Descripción Producto", "Categoría",
                                       "Precio", "Stock Mínimo", "Stock Máximo", "Fecha Movimiento", "Tipo",
                                       "Cantidad", "ID Proveedor", "Remitente"])

                movimientos = obtener_movimientos()
                for movimiento in movimientos:
                    ws_movimientos.append(movimiento)

                ws_proveedores = wb.create_sheet(title="Proveedores")
                ws_proveedores.append(["ID Proveedor", "Nombre", "Apellido", "Dirección", "Teléfono", "Email"])

                proveedores = obtener_proveedores()
                for proveedor in proveedores:
                    ws_proveedores.append(proveedor)

                wb.save(file_path)
                QMessageBox.information(self, "Exportar Movimientos", "Los movimientos se exportaron correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Exportar Movimientos", f"Error al exportar los movimientos: {str(e)}")

    def guardar_movimiento(self):
        try:
            NombreProducto = self.NombreProducto_input.text()
            DescripcionProducto = self.DescripcionProducto_input.text()
            CategoriaProducto = self.CategoriaProducto_input.currentText()
            PrecioProducto = float(self.PrecioProducto_input.text())
            StockMinimoProducto = 5
            StockMaximoProducto = 100
            FechaMovimiento = obtener_fecha()[0]
            TipoMovimiento = self.TipoMovimiento_input.currentText()
            Cantidad = int(self.Cantidad_input.text())
            ProveedorID = self.ProveedorID_input.text() if self.ProveedorID_input.text() else None
            Remitente = self.Remitente_input.text() if self.TipoMovimiento_input.currentText() == "Salida" else None

            guardar_movimiento(NombreProducto, DescripcionProducto, CategoriaProducto, PrecioProducto,
                               StockMinimoProducto, StockMaximoProducto, FechaMovimiento, TipoMovimiento, Cantidad,
                               ProveedorID, Remitente)
            self.cargar_movimiento()
            self.limpiar_campos()
        except ValueError:
            QMessageBox.warning(self, "Agregar Movimiento", "Por favor, ingrese un valor válido para el precio o la cantidad.")

    def seleccionar_movimiento(self, row, column):
        try:
            if 0 <= row < self.table.rowCount() and 0 <= column < self.table.columnCount():
                self.NombreProducto_input.setText(self.table.item(row, 1).text())
                self.DescripcionProducto_input.setText(self.table.item(row, 2).text())
                self.CategoriaProducto_input.setCurrentText(self.table.item(row, 3).text())
                self.PrecioProducto_input.setText(self.table.item(row, 4).text())
                self.TipoMovimiento_input.setCurrentText(self.table.item(row, 8).text())
                self.Cantidad_input.setText(self.table.item(row, 9).text())
                self.ProveedorID_input.setText(self.table.item(row, 10).text())
                self.Remitente_input.setText(self.table.item(row, 11).text())
            else:
                print("Índices de fila y/o columna fuera de los límites válidos.")
        except Exception as e:
            print("Error al seleccionar movimiento:", e)

    def actualizar_movimiento(self):
        try:
            NombreProducto = self.NombreProducto_input.text()
            DescripcionProducto = self.DescripcionProducto_input.text()
            CategoriaProducto = self.CategoriaProducto_input.currentText()
            PrecioProducto = float(self.PrecioProducto_input.text())
            StockMinimoProducto = 5
            StockMaximoProducto = 100
            FechaMovimiento = obtener_fecha()[0]
            TipoMovimiento = self.TipoMovimiento_input.currentText()
            Cantidad = int(self.Cantidad_input.text())
            ProveedorID = self.ProveedorID_input.text() if self.ProveedorID_input.text() else None
            Remitente = self.Remitente_input.text() if self.TipoMovimiento_input.currentText() == "Salida" else None

            fila_seleccionada = self.table.currentRow()
            if fila_seleccionada == -1:
                QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un movimiento de la tabla.")
                return

            movimiento_id = self.table.item(fila_seleccionada, 0).text()
            actualizar_movimiento(movimiento_id, NombreProducto, DescripcionProducto, CategoriaProducto,
                                  PrecioProducto, StockMinimoProducto, StockMaximoProducto, FechaMovimiento,
                                  TipoMovimiento, Cantidad, ProveedorID, Remitente)
            self.cargar_movimiento()
            self.limpiar_campos()
        except ValueError:
            QMessageBox.warning(self, "Actualizar Movimiento", "Por favor, ingrese un valor válido para el precio o la cantidad.")

    def eliminar_movimiento(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un proveedor de la tabla.")
            return

        movimiento_id = self.table.item(fila_seleccionada, 0).text()
        eliminar_movimiento(movimiento_id)
        self.cargar_movimiento()
        self.limpiar_campos()

    def cargar_movimiento(self):
        self.table.setRowCount(0)
        movimientos = obtener_movimientos()
        for row, movimiento in enumerate(movimientos):
            self.table.insertRow(row)
            for column, data in enumerate(movimiento):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def limpiar_campos(self):
        self.NombreProducto_input.clear()
        self.DescripcionProducto_input.clear()
        self.PrecioProducto_input.clear()
        self.Cantidad_input.clear()
        self.ProveedorID_input.clear()
        self.Remitente_input.clear()

    def actualizar_campos(self):
        if self.TipoMovimiento_input.currentText() == "Entrada":
            self.ProveedorID_input.show()
            self.Remitente_input.hide()
        elif self.TipoMovimiento_input.currentText() == "Salida":
            self.ProveedorID_input.hide()
            self.Remitente_input.show()
            self.ProveedorID_input.clear()
        else:
            self.ProveedorID_input.hide()
            self.Remitente_input.hide()

    def obtener_fecha(self):
        fecha = obtener_fecha()
        self.FechaMovimiento_input.setText(str(fecha[0]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
