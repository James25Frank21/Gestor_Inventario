import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from DAO.proveedoresDAO import guardar_proveedor, obtener_proveedores, actualizar_proveedor, eliminar_proveedor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestión de Inventario")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Introduce la información del proveedor:")
        self.layout.addWidget(self.label)

        self.nombre_label = QLabel("Nombre:")
        self.layout.addWidget(self.nombre_label)
        self.nombre_input = QLineEdit()
        self.layout.addWidget(self.nombre_input)

        self.apellido_label = QLabel("Apellido:")
        self.layout.addWidget(self.apellido_label)
        self.apellido_input = QLineEdit()
        self.layout.addWidget(self.apellido_input)

        self.direccion_label = QLabel("Dirección:")
        self.layout.addWidget(self.direccion_label)
        self.direccion_input = QLineEdit()
        self.layout.addWidget(self.direccion_input)

        self.telefono_label = QLabel("Teléfono:")
        self.layout.addWidget(self.telefono_label)
        self.telefono_input = QLineEdit()
        self.layout.addWidget(self.telefono_input)

        self.email_label = QLabel("Email:")
        self.layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_input)

        self.guardar_button = QPushButton("Guardar Proveedor")
        self.guardar_button.clicked.connect(self.guardar_proveedor)
        self.layout.addWidget(self.guardar_button)

        self.actualizar_button = QPushButton("Actualizar")
        self.actualizar_button.clicked.connect(self.actualizar_proveedor)
        self.layout.addWidget(self.actualizar_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre","Apellido", "Dirección", "Teléfono", "Email"])
        self.table.cellClicked.connect(self.seleccionar_proveedor)
        self.layout.addWidget(self.table)

        self.cargar_proveedores()

    def guardar_proveedor(self):
        nombre = self.nombre_input.text()
        apellido = self.apellido_input.text()
        direccion = self.direccion_input.text()
        telefono = self.telefono_input.text()
        email = self.email_input.text()

        guardar_proveedor(nombre,apellido, direccion, telefono, email)
        self.cargar_proveedores()
        self.limpiar_campos()

    def seleccionar_proveedor(self, row, column):
        self.nombre_input.setText(self.table.item(row, 0).text())
        self.apellido_input.setText(self.table.item(row, 1).text())
        self.direccion_input.setText(self.table.item(row, 2).text())
        self.telefono_input.setText(self.table.item(row, 3).text())
        self.email_input.setText(self.table.item(row, 4).text())

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

        id_proveedor = self.table.item(fila_seleccionada, 0).text()  # Supongo que el ID del proveedor está en la primera columna
        actualizar_proveedor(id_proveedor, nombre, apellido, direccion, telefono, email)
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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
