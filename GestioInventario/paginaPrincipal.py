import sys
from PyQt6.QtGui import QAction, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QWidget
from proveedoresUI import *
from registroMovimientoUI import MainWindowM
from userUI import MainWindowU
from login import *

class MainWindowPri(QMainWindow):
    def __init__(self, rol):
        super().__init__()
        self.setWindowTitle("Gestión de Usuarios")
        self.setWindowIcon(QIcon("img/pngegg (5).png"))
        self.setGeometry(350, 100, 630, 550)

        #esta parte captura el rol del usuario
        self.rol = rol
        print(self.rol)

        self.setWindowTitle("Barra de Navegación")

        # Creamos acciones para las opciones del menú
        self.createActions()

        # Creamos la barra de herramientas
        self.createToolBar()

        # Creamos el diseño principal de la ventana
        self.createLayout()

    def createActions(self):
        # Creamos una acción para la opción "Inicio"
        self.action_inicio = QAction(QIcon("img/iconos/hogar.png"),"Inicio", self)
        self.action_inicio.triggered.connect(self.inicio)

        self.action_usuario = QAction(QIcon("img/iconos/archivo-hoja-de-calculo.png"),"Exportar Excel", self)
        self.action_usuario.triggered.connect(self.abrir_interfaz_movimientoExcel)

        self.action_salir = QAction(QIcon("img/iconos/salida-del-portal.png"),"Cerrar sesión", self)
        self.action_salir.triggered.connect(self.salir)

    def createToolBar(self):
        # Creamos la barra de herramientas y agregamos las acciones
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(self.action_inicio)
        self.toolbar.addAction(self.action_usuario)
        self.toolbar.addAction(self.action_salir)

    def createLayout(self):
        main_layout = QHBoxLayout()

        # Layout vertical para los botones
        buttons_layout = QVBoxLayout()

        #botones
        self.añadirProveedor = QPushButton("Registrar Proveedor", self)
        self.añadirProveedor.clicked.connect(self.abrir_interfaz_proveedores)
        self.añaditMovimiento = QPushButton("Registrar Movimiento", self)
        self.añaditMovimiento.clicked.connect(self.abrir_interfaz_movimiento)
        self.añadirUsuario = QPushButton("Registrar Usuario", self)
        self.añadirUsuario.clicked.connect(self.abrir_interfaz_user)


        if self.rol == "Usuario":
            self.añadirUsuario.setVisible(False)
        else:
            self.añadirUsuario.setVisible(True)

        # en esta parte se establece estilos para los botones
        self.añadirProveedor.setStyleSheet("background-color: #4CAF50; color: white;")
        self.añaditMovimiento.setStyleSheet("background-color: #008CBA; color: white;")
        self.añadirUsuario.setStyleSheet("background-color: #f44336; color: white;")

        # se establece el tamaño de los botones
        button_size = (200, 40)
        self.añadirProveedor.setFixedSize(*button_size)
        self.añaditMovimiento.setFixedSize(*button_size)
        self.añadirUsuario.setFixedSize(*button_size)

        # Para agregar los botones al layout vertical
        buttons_layout.addWidget(self.añadirProveedor)
        buttons_layout.addWidget(self.añaditMovimiento)
        buttons_layout.addWidget(self.añadirUsuario)

        # Imagen
        image_label = QLabel()
        pixmap = QPixmap("img/imagen.png")
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setFixedSize(400, 380)

        #layout de botones al layout principal
        main_layout.addLayout(buttons_layout)

        #espacio entre los botones y la imagen
        main_layout.addSpacing(20)

        #imagen al layout principal
        main_layout.addWidget(image_label)

        #layout principal de la ventana
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)



    def inicio(self):
        self.statusBar().showMessage("Calichin usted se encuentra en la página de inicio...")



    def salir(self):
        self.close()



    def abrir_interfaz_proveedores(self):
        self.interfaz_proveedores = MainWindowP()
        self.interfaz_proveedores.show()


    def abrir_interfaz_movimiento(self):
        self.interfaz_movimiento = MainWindowM()
        self.interfaz_movimiento.show()


    def abrir_interfaz_movimientoExcel(self):
        self.interfaz_movimiento = MainWindowM()
        self.interfaz_movimiento.exportar_movimiento()


    def abrir_interfaz_user(self):
        self.interfaz_user = MainWindowU()
        self.interfaz_user.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindowPri("")
    window.show()
    sys.exit(app.exec())
