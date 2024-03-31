from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QFormLayout, QWidget, QHBoxLayout, QPushButton, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox
from PyQt6.QtGui import QPixmap, QIcon
from DAO.userDAO import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Inventario")

        self.setWindowIcon(QIcon("img/pngegg (5).png"))
        self.layout = QVBoxLayout()
        self.setGeometry(350, 100, 360, 380)


        self.form_layout = QFormLayout()


        self.registro_label = QLabel("Registro de Usuarios")
        self.form_layout.addRow(self.registro_label)
        self.registro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.form_layout.addRow(QLabel(""))

        #Campos de texto
        self.nombreUsuario_input = QLineEdit()
        self.form_layout.addRow(QLabel("Nombre:"), self.nombreUsuario_input)

        self.contrasena_input = QLineEdit()
        self.form_layout.addRow(QLabel("Contraseña:"), self.contrasena_input)

        # ComboBox para el rol del usuario 'Admin', 'Usuario'
        self.rol_input = QComboBox()
        rol = ['Admin', 'Usuario']
        self.rol_input.addItems(rol)
        self.form_layout.addRow(QLabel("Rol:"), self.rol_input)

        #para el tamaño de los campos de texto
        for i in range(self.form_layout.rowCount()):
            self.form_layout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().setFixedWidth(140)

        #organizar los campos
        self.form_layout.addRow(QLabel(""))
        #layout vertical para los botones
        layout_vbox_buttons = QHBoxLayout()
        self.form_layout.addRow(layout_vbox_buttons)
        # salto de línea
        self.form_layout.addRow(QLabel(""))

        # Crear botones
        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")

        self.add_button.clicked.connect(self.guardar_user)
        self.update_button.clicked.connect(self.actualizar_user)
        self.delete_button.clicked.connect(self.eliminar_user)

        #botones vertical
        layout_vbox_buttons.addWidget(self.add_button)
        layout_vbox_buttons.addWidget(self.update_button)
        layout_vbox_buttons.addWidget(self.delete_button)

        #tamaño de los botones
        self.add_button.setFixedSize(70, 22)
        self.update_button.setFixedSize(70, 22)
        self.delete_button.setFixedSize(70, 22)

        #ayout horizontal para el formulario y los botones
        layout_hbox = QHBoxLayout()
        layout_hbox.addLayout(self.form_layout)
        layout_hbox.addLayout(layout_vbox_buttons)

        #imagen
        self.image_label = QLabel()
        pixmap = QPixmap("img/pngegg (3).png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        #tamaño de la imagen
        self.image_label.setFixedSize(190, 140)

        #layout vertical principal
        layout_vbox = QVBoxLayout()

        #layout horizontal y la imagen al layout vertical principal
        layout_vbox.addLayout(layout_hbox)
        layout_hbox.addWidget(self.image_label)

        #tabla
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["UsuarioID", "NombreUsuario", "Contraseña", "Rol"])
        self.table.cellClicked.connect(self.seleccionar_user)
        self.cargar_user()

        #tabla al layout vertical
        layout_vbox.addWidget(self.table)

        #layout vertical principal
        self.setLayout(layout_vbox)

    #botones a sus respectivas funciones
    def guardar_user(self):
        NombreUsuario = self.nombreUsuario_input.text()
        Contraseña = self.contrasena_input.text()
        Rol = self.rol_input.currentText()

        guardar_usuario(NombreUsuario, Contraseña, Rol)
        self.cargar_user()
        self.limpiar_campos()

    def seleccionar_user(self, row, column):
        self.nombreUsuario_input.setText(self.table.item(row, 1).text())
        self.contrasena_input.setText(self.table.item(row, 2).text())
        self.rol_input.setCurrentText(self.table.item(row, 3).text())

    def actualizar_user(self):
        NombreUsuario = self.nombreUsuario_input.text()
        Contraseña = self.contrasena_input.text()
        Rol = self.rol_input.currentText()

        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un Usuario de la tabla.")
            return

        usuario_id = self.table.item(fila_seleccionada, 0).text()
        actualizar_usuario(usuario_id, NombreUsuario, Contraseña, Rol)
        self.cargar_user()
        self.limpiar_campos()

    def eliminar_user(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un Usuario de la tabla.")
            return

        usuario_id = self.table.item(fila_seleccionada, 0).text()
        eliminar_usuario(usuario_id)
        self.cargar_user()
        self.limpiar_campos()

    def cargar_user(self):
        self.table.setRowCount(0)
        usuarios = obtener_usuarios()
        for row, usuario in enumerate(usuarios):
            self.table.insertRow(row)
            for column, data in enumerate(usuario):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def limpiar_campos(self):
        self.nombreUsuario_input.clear()
        self.contrasena_input.clear()
        self.rol_input.setCurrentIndex(0)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
