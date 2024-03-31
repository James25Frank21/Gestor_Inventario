from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QFormLayout, QWidget, QHBoxLayout, QPushButton, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QMainWindow, QToolBar
from PyQt6.QtGui import QPixmap, QIcon, QAction
from DAO.userDAO import UsuarioDAO
from model.User import *
from registroMovimientoUI import MainWindowM


class MainWindowU(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Usuarios")
        self.setWindowIcon(QIcon("img/pngegg (5).png"))
        self.setGeometry(350, 100, 360, 380)

        # Configurar el formulario
        self.form_layout = QFormLayout()

        # Título del formulario
        self.registro_label = QLabel("Registro de Usuarios")
        self.form_layout.addRow(self.registro_label)
        self.registro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Campos de texto
        self.nombreUsuario_input = QLineEdit()
        self.form_layout.addRow(QLabel("Nombre:"), self.nombreUsuario_input)

        self.contrasena_input = QLineEdit()
        self.form_layout.addRow(QLabel("Contraseña:"), self.contrasena_input)

        # ComboBox para el rol del usuario 'Admin', 'Usuario'
        self.rol_input = QComboBox()
        rol = ['Admin', 'Usuario']
        self.rol_input.addItems(rol)
        self.form_layout.addRow(QLabel("Rol:"), self.rol_input)

        # Para el tamaño de los campos de texto
        for i in range(self.form_layout.rowCount()):
            self.form_layout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().setFixedWidth(140)

        # Organizar los campos
        self.form_layout.addRow(QLabel(""))

        # Layout vertical para los botones
        layout_vbox_buttons = QHBoxLayout()
        self.form_layout.addRow(layout_vbox_buttons)

        # Salto de línea
        self.form_layout.addRow(QLabel(""))

        # Crear botones
        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")

        self.add_button.clicked.connect(self.guardar_usuario)
        self.update_button.clicked.connect(self.actualizar_usuario)
        self.delete_button.clicked.connect(self.eliminar_usuario)

        # Botones vertical
        layout_vbox_buttons.addWidget(self.add_button)
        layout_vbox_buttons.addWidget(self.update_button)
        layout_vbox_buttons.addWidget(self.delete_button)

        # Tamaño de los botones
        self.add_button.setFixedSize(70, 22)
        self.update_button.setFixedSize(70, 22)
        self.delete_button.setFixedSize(70, 22)

        # Layout horizontal para el formulario y los botones
        layout_hbox = QHBoxLayout()
        layout_hbox.addLayout(self.form_layout)

        # Imagen
        self.image_label = QLabel()
        pixmap = QPixmap("img/pngegg (3).png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        # Tamaño de la imagen
        self.image_label.setFixedSize(190, 140)

        # Agregar la imagen al layout horizontal
        layout_hbox.addWidget(self.image_label)

        # Layout vertical principal
        layout_vbox = QVBoxLayout()

        # Agregar el layout horizontal al vertical principal
        layout_vbox.addLayout(layout_hbox)

        # Tabla de usuarios
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["UsuarioID", "NombreUsuario", "Contraseña", "Rol"])
        self.table.cellClicked.connect(self.seleccionar_usuario)
        self.cargar_usuarios()

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
    def guardar_usuario(self):
        nombre_usuario = self.nombreUsuario_input.text()
        contraseña = self.contrasena_input.text()
        rol = self.rol_input.currentText()

        usuario = Usuario(None, nombre_usuario, contraseña, rol)
        UsuarioDAO.guardar_usuario(usuario)
        self.cargar_usuarios()
        self.limpiar_campos()

    def seleccionar_usuario(self, row, column):
        self.nombreUsuario_input.setText(self.table.item(row, 1).text())
        self.contrasena_input.setText(self.table.item(row, 2).text())
        self.rol_input.setCurrentText(self.table.item(row, 3).text())

    def actualizar_usuario(self):
        nombre_usuario = self.nombreUsuario_input.text()
        contraseña = self.contrasena_input.text()
        rol = self.rol_input.currentText()

        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un Usuario de la tabla.")
            return

        usuario_id = int(self.table.item(fila_seleccionada, 0).text())
        usuario = Usuario(usuario_id, nombre_usuario, contraseña, rol)
        UsuarioDAO.actualizar_usuario(usuario)
        self.cargar_usuarios()
        self.limpiar_campos()

    def eliminar_usuario(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un Usuario de la tabla.")
            return

        usuario_id = int(self.table.item(fila_seleccionada, 0).text())
        UsuarioDAO.eliminar_usuario(usuario_id)
        self.cargar_usuarios()
        self.limpiar_campos()

    def cargar_usuarios(self):
        self.table.setRowCount(0)
        usuarios = UsuarioDAO.obtener_usuarios()
        for row, usuario in enumerate(usuarios):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(usuario.usuario_id)))
            self.table.setItem(row, 1, QTableWidgetItem(usuario.nombre_usuario))
            self.table.setItem(row, 2, QTableWidgetItem(usuario.contraseña))
            self.table.setItem(row, 3, QTableWidgetItem(usuario.rol))

    def limpiar_campos(self):
        self.nombreUsuario_input.clear()
        self.contrasena_input.clear()
        self.rol_input.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindowU()
    window.show()
    app.exec()
