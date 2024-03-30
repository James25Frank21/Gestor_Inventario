from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QFormLayout, QWidget, QHBoxLayout, QPushButton, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from DAO.proveedoresDAO import guardar_proveedor, obtener_proveedores, actualizar_proveedor, eliminar_proveedor


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Inventario")
        # Agregar un icono a la ventana
        self.setWindowIcon(QIcon("img/pngegg (5).png"))
        self.layout = QVBoxLayout()
        self.setGeometry(350, 100, 630, 550)#fijar tamaño de la ventana


        # Configurar el formulario
        self.form_layout = QFormLayout()



        # Agregar el título "Registro de Proveedores"
        self.registro_label = QLabel("Registro de Proveedores")
        self.form_layout.addRow(self.registro_label)

        # Agregar campos
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

        #insertar un salto de linea
        self.form_layout.addRow(QLabel(""))
        # Crear el layout vertical para los botones
        layout_vbox_buttons = QHBoxLayout()
        # Agregar el botones_layout
        self.form_layout.addRow(layout_vbox_buttons)

        # Crear botones
        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")

        self.add_button.clicked.connect(self.guardar_proveedor)


        self.update_button.clicked.connect(self.actualizar_proveedor)


        self.delete_button.clicked.connect(self.eliminar_proveedor)


        # Agregar los botones al layout vertical
        layout_vbox_buttons.addWidget(self.add_button)
        layout_vbox_buttons.addWidget(self.update_button)
        layout_vbox_buttons.addWidget(self.delete_button)


        #cambiar el tamaño de los botones
        self.add_button.setFixedSize(80, 30)
        self.update_button.setFixedSize(80, 30)
        self.delete_button.setFixedSize(80, 30)

        # Crear un layout horizontal para el formulario y los botones
        layout_hbox = QHBoxLayout()
        layout_hbox.addLayout(self.form_layout)
        layout_hbox.addLayout(layout_vbox_buttons)

        # Crear la imagen
        self.image_label = QLabel()
        pixmap = QPixmap("img/pngegg.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        # Cambiar el tamaño de la imagen
        self.image_label.setFixedSize(300, 250)

        # Crear el layout vertical principal
        layout_vbox = QVBoxLayout()

        # Agregar el layout horizontal y la imagen al layout vertical principal
        layout_vbox.addLayout(layout_hbox)
        layout_hbox.addWidget(self.image_label)



        # Crear la tabla
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ProveedorID", "Nombre", "Apellido", "Dirección", "Teléfono", "Email"])
        self.table.cellClicked.connect(self.seleccionar_proveedor)


        self.cargar_proveedores()

        # Agregar la tabla al layout vertical
        layout_vbox.addWidget(self.table)

        # Establecer el layout vertical principal como el layout principal
        self.setLayout(layout_vbox)


    # Conectar los botones a sus respectivas funciones
    def guardar_proveedor(self):
        nombre = self.nombre_input.text()
        apellido = self.apellido_input.text()
        direccion = self.direccion_input.text()
        telefono = self.telefono_input.text()
        email = self.email_input.text()

        guardar_proveedor(nombre, apellido, direccion, telefono, email)
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

        id_proveedor = self.table.item(fila_seleccionada, 0).text()
        actualizar_proveedor(id_proveedor, nombre, apellido, direccion, telefono, email)
        self.cargar_proveedores()
        self.limpiar_campos()

    def eliminar_proveedor(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un proveedor de la tabla.")
            return

        id_proveedor = self.table.item(fila_seleccionada, 0).text()
        eliminar_proveedor(id_proveedor)
        self.cargar_proveedores()
        self.limpiar_campos()

    def cargar_proveedores(self):
        self.table.setRowCount(0)
        proveedores = obtener_proveedores()
        for row, proveedor in enumerate(proveedores):
            self.table.insertRow(row)
            for column, data in enumerate(proveedor):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def limpiar_campos(self):
        self.nombre_input.clear()
        self.apellido_input.clear()
        self.direccion_input.clear()
        self.telefono_input.clear()
        self.email_input.clear()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()