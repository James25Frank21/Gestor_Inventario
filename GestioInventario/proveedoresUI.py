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


        self.form_layout = QFormLayout() #esto sirve para que los campos del formulario queden en forma de tabla

        # Esta parte es para el formulario
        self.registro_label = QLabel("Registro de Proveedores")
        self.form_layout.addRow(self.registro_label)

        # Campos del formulario
        self.nombre_input = QLineEdit()
        self.form_layout.addRow(QLabel("Nombre:"), self.nombre_input)

        self.direccion_input = QLineEdit()
        self.form_layout.addRow(QLabel("Dirección:"), self.direccion_input)

        self.telefono_input = QLineEdit()
        self.form_layout.addRow(QLabel("Teléfono:"), self.telefono_input)

        self.email_input = QLineEdit()
        self.form_layout.addRow(QLabel("Email:"), self.email_input)

        # esto es para que los campos del formulario tengan un tamaño fijo
        for i in range(self.form_layout.rowCount()):
            self.form_layout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().setFixedWidth(200)


        self.form_layout.addRow(QLabel("")) #esto es para que haya un espacio entre los campos del formulario y los botones

        layout_vbox_buttons = QHBoxLayout() #esto me permite poner los botones en una fila horizontal
        self.form_layout.addRow(layout_vbox_buttons)

        #En esta parte se crean los botones
        self.agregarBtn = QPushButton("Agregar")
        self.actualizarBtn = QPushButton("Actualizar")
        self.eliminarBtn = QPushButton("Eliminar")

        self.agregarBtn.clicked.connect(self.guardar_proveedor)
        self.actualizarBtn.clicked.connect(self.actualizar_proveedor)
        self.eliminarBtn.clicked.connect(self.eliminar_proveedor)

        #Aqui se agregan los botones
        layout_vbox_buttons.addWidget(self.agregarBtn)#vbox es para que los botones queden uno debajo del otro
        layout_vbox_buttons.addWidget(self.actualizarBtn)
        layout_vbox_buttons.addWidget(self.eliminarBtn)

        #en esta parte se le da un tamaño fijo a los botones
        self.agregarBtn.setFixedSize(80, 30)
        self.actualizarBtn.setFixedSize(80, 30)
        self.eliminarBtn.setFixedSize(80, 30)


        layout_hbox = QHBoxLayout() # esto es para que la imagen y el formulario queden en una fila horizontal
        layout_hbox.addLayout(self.form_layout)

        #Imagen
        self.image_label = QLabel()
        pixmap = QPixmap("img/pngegg.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        #en esta parte se le da un tamaño fijo a la imagen
        self.image_label.setFixedSize(300, 250)


        layout_hbox.addWidget(self.image_label) #esto es para que la imagen y el formulario queden en una fila horizontal


        layout_vbox = QVBoxLayout() # esto es para que la tabla y el formulario queden en una fila vertical
        layout_vbox.addLayout(layout_hbox)

        # Tabla de proveedores
        self.table = QTableWidget()
        self.table.setColumnCount(5)#esto es para que la tabla tenga 5 columnas
        self.table.setHorizontalHeaderLabels(["ProveedorID", "Nombre", "Dirección", "Teléfono", "Email"])
        self.table.cellClicked.connect(self.seleccionar_proveedor)
        self.cargar_proveedores()

        # esto es para que la tabla y el formulario queden en una fila vertical
        layout_vbox.addWidget(self.table)
        widget = QWidget()
        widget.setLayout(layout_vbox)
        self.setCentralWidget(widget)

        #barra de herramientas (ToolBar)
        self.toolbar = QToolBar("ToolBar")
        self.addToolBar(self.toolbar)

        # Acciones de la barra de herramientas
        self.action_inicio = QAction(QIcon("img/iconos/hogar.png"), "Inicio", self)
        self.action_Exportar = QAction(QIcon("img/iconos/archivo-hoja-de-calculo.png"), "Exportar Excel", self)
        self.action_salir = QAction(QIcon("img/iconos/salida-del-portal.png"), "Salir", self)

        self.action_inicio.triggered.connect(self.inicio)
        self.action_Exportar.triggered.connect(self.abrir_interfaz_movimientoExcel)
        self.action_salir.triggered.connect(self.salir)

        #esta parte es para darle a los iconos una accion
        self.toolbar.addAction(self.action_inicio)
        self.toolbar.addAction(self.action_Exportar)
        self.toolbar.addAction(self.action_salir)

    def inicio(self):
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
        direccion = self.direccion_input.text()
        telefono = self.telefono_input.text()
        email = self.email_input.text()

        proveedor = Proveedor(None, nombre, direccion, telefono, email)
        ProveedorDAO.insertar_proveedor(proveedor)
        self.cargar_proveedores()
        self.limpiar_campos()

    def seleccionar_proveedor(self, row, column):
        self.nombre_input.setText(self.table.item(row, 1).text())
        self.direccion_input.setText(self.table.item(row, 3).text())
        self.telefono_input.setText(self.table.item(row, 4).text())
        self.email_input.setText(self.table.item(row, 5).text())

    def actualizar_proveedor(self):
        nombre = self.nombre_input.text()
        direccion = self.direccion_input.text()
        telefono = self.telefono_input.text()
        email = self.email_input.text()

        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "WIU wiu wiu Ojito", "seleccione un proveedor de la tabla.")
            return

        id_proveedor = int(self.table.item(fila_seleccionada, 0).text())
        proveedor = Proveedor(id_proveedor, nombre, direccion, telefono, email)
        ProveedorDAO.actualizar_proveedor(proveedor)
        self.cargar_proveedores()
        self.limpiar_campos()

    def eliminar_proveedor(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "WIU wiu wiu Ojito", "seleccione un proveedor de la tabla.")
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
            self.table.setItem(row, 2, QTableWidgetItem(proveedor.direccion))
            self.table.setItem(row, 3, QTableWidgetItem(proveedor.telefono))
            self.table.setItem(row, 4, QTableWidgetItem(proveedor.email))

    def limpiar_campos(self):
        self.nombre_input.clear()
        self.direccion_input.clear()
        self.telefono_input.clear()
        self.email_input.clear()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindowP()
    window.show()
    app.exec()
