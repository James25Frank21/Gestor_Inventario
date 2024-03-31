from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QFormLayout, QMainWindow, QHBoxLayout, QPushButton, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QToolBar, QWidget
from PyQt6.QtGui import QPixmap, QIcon, QAction
from DAO.proveedoresDAO import ProveedorDAO
from model.Proveedores import *
from paginaPrincipal import *
from registroMovimientoUI import MainWindowM


class MainWindowP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Inventario")
        self.setWindowIcon(QIcon("img/pngegg (5).png"))
        self.setGeometry(350, 100, 630, 550)

        # Configurar el formulario
        self.form_layout = QFormLayout()

        # Título del formulario
        self.registro_label = QLabel("Registro de Proveedores")
        self.form_layout.addRow(self.registro_label)

        # Campos del formulario
        self.nombre_input = QLineEdit()
        self.form_layout.addRow(QLabel("Nombre:"), self.nombre_input)

        self.apellido_input = QLineEdit()
        self.form_layout.addRow(QLabel("Apellido:"), self.apellido_input)

        self.direccion_input = QLineEdit()
        self.form_layout.addRow(QLabel("Dirección:"), self.direccion_input)

        self.telefono_input = QLineEdit()
        self.form_layout.addRow(QLabel("Teléfono:"), self.telefono_input)

        self.email_input = QLineEdit()
        self.form_layout.addRow(QLabel("Email:"), self.email_input)

        # Cambiar el tamaño de los campos
        for i in range(self.form_layout.rowCount()):
            self.form_layout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().setFixedWidth(200)

        # Salto de línea
        self.form_layout.addRow(QLabel(""))
        # Layout vertical para los botones
        layout_vbox_buttons = QHBoxLayout()
        self.form_layout.addRow(layout_vbox_buttons)

        # Botones
        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")

        self.add_button.clicked.connect(self.guardar_proveedor)
        self.update_button.clicked.connect(self.actualizar_proveedor)
        self.delete_button.clicked.connect(self.eliminar_proveedor)

        # Botones en el layout vertical
        layout_vbox_buttons.addWidget(self.add_button)
        layout_vbox_buttons.addWidget(self.update_button)
        layout_vbox_buttons.addWidget(self.delete_button)

        # Tamaño de los botones
        self.add_button.setFixedSize(80, 30)
        self.update_button.setFixedSize(80, 30)
        self.delete_button.setFixedSize(80, 30)

        # Layout horizontal para el formulario y los botones
        layout_hbox = QHBoxLayout()
        layout_hbox.addLayout(self.form_layout)

        # Imagen
        self.image_label = QLabel()
        pixmap = QPixmap("img/pngegg.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        # Tamaño de la imagen
        self.image_label.setFixedSize(300, 250)

        # Agregar la imagen al layout horizontal
        layout_hbox.addWidget(self.image_label)

        # Layout vertical principal
        layout_vbox = QVBoxLayout()

        # Agregar el layout horizontal al vertical principal
        layout_vbox.addLayout(layout_hbox)

        # Tabla de proveedores
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ProveedorID", "Nombre", "Apellido", "Dirección", "Teléfono", "Email"])
        self.table.cellClicked.connect(self.seleccionar_proveedor)
        self.cargar_proveedores()

        # Agregar la tabla al layout vertical
        layout_vbox.addWidget(self.table)
        widget = QWidget()
        widget.setLayout(layout_vbox)
        self.setCentralWidget(widget)

        # Crear la barra de herramientas (ToolBar)
        self.toolbar = QToolBar("ToolBar")
        self.addToolBar(self.toolbar)

        # Acciones de la barra de herramientas
        self.action_inicio = QAction(QIcon("home.png"), "Inicio", self)
        self.action_Exportar = QAction(QIcon("save.png"), "Exportar Excel", self)
        self.action_salir = QAction(QIcon("exit.png"), "Salir", self)

        self.action_inicio.triggered.connect(self.on_inicio)
        self.action_Exportar.triggered.connect(self.abrir_interfaz_movimientoExcel)
        self.action_salir.triggered.connect(self.salir)

        # Agregar acciones a la barra de herramientas
        self.toolbar.addAction(self.action_inicio)
        self.toolbar.addAction(self.action_Exportar)
        self.toolbar.addAction(self.action_salir)
    def on_inicio(self):
        self.statusBar().showMessage("Usted se encuentra en la página de inicio...")
        self.close()


    def salir(self):
        QApplication.quit()

    def abrir_interfaz_movimientoExcel(self):
        self.interfaz_movimiento = MainWindowM()
        self.interfaz_movimiento.exportar_movimiento()
    # Funciones de los botones
    def guardar_proveedor(self):
        nombre = self.nombre_input.text()
        apellido = self.apellido_input.text()
        direccion = self.direccion_input.text()
        telefono = self.telefono_input.text()
        email = self.email_input.text()

        proveedor = Proveedor(None, nombre, apellido, direccion, telefono, email)
        ProveedorDAO.insertar_proveedor(proveedor)
        self.cargar_proveedores()
        self.limpiar_campos()

    def seleccionar_proveedor(self, row, column):
        self.nombre_input.setText(self.table.item(row, 1).text())
        self.apellido_input.setText(self.table.item(row, 2).text())
        self.direccion_input.setText(self.table.item(row, 3).text())
        self.telefono_input.setText(self.table.item(row, 4).text())
        self.email_input.setText(self.table.item(row, 5).text())

    def actualizar_proveedor(self):
        nombre = self.nombre_input.text()
        apellido = self.apellido_input.text()
        direccion = self.direccion_input.text()
        telefono = self.telefono_input.text()
        email = self.email_input.text()

        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un proveedor de la tabla.")
            return

        id_proveedor = int(self.table.item(fila_seleccionada, 0).text())
        proveedor = Proveedor(id_proveedor, nombre, apellido, direccion, telefono, email)
        ProveedorDAO.actualizar_proveedor(proveedor)
        self.cargar_proveedores()
        self.limpiar_campos()

    def eliminar_proveedor(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un proveedor de la tabla.")
            return

        id_proveedor = int(self.table.item(fila_seleccionada, 0).text())
        ProveedorDAO.eliminar_proveedor(id_proveedor)
        self.cargar_proveedores()
        self.limpiar_campos()

    def cargar_proveedores(self):
        self.table.setRowCount(0)
        proveedores = ProveedorDAO.obtener_proveedores()
        for row, proveedor in enumerate(proveedores):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(proveedor.proveedor_id)))
            self.table.setItem(row, 1, QTableWidgetItem(proveedor.nombre))
            self.table.setItem(row, 2, QTableWidgetItem(proveedor.apellido))
            self.table.setItem(row, 3, QTableWidgetItem(proveedor.direccion))
            self.table.setItem(row, 4, QTableWidgetItem(proveedor.telefono))
            self.table.setItem(row, 5, QTableWidgetItem(proveedor.email))

    def limpiar_campos(self):
        self.nombre_input.clear()
        self.apellido_input.clear()
        self.direccion_input.clear()
        self.telefono_input.clear()
        self.email_input.clear()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindowP()
    window.show()
    app.exec()
