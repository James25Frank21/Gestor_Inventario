import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from DAO.userDAO import *
from paginaPrincipal import *


class LoginR(QWidget):

    def __init__(self):
        super().__init__()
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setGeometry(500, 200, 350, 450)
        self.setWindowTitle("Gestión de inventarios")
        self.setWindowIcon(QIcon("img/pngegg (5).png"))
        self.FondoImagen("img/pngegg (4).png")
        self.generar_formulario()
        self.show()

    def FondoImagen(self, image_path):
        palette = self.palette()
        background_image = QPixmap(image_path)
        palette.setBrush(QPalette.ColorRole.Window,
                         QBrush(background_image.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)))
        self.setPalette(palette)

    def generar_formulario(self):
        self.is_logged = False

        tittle_label = QLabel(self)
        tittle_label.setText("Iniciar sesión")
        tittle_label.setFont(QFont('Medio', 20))
        tittle_label.setStyleSheet("color:white;")
        tittle_label.move(100, 70)

        user_label = QLabel(self)
        user_label.setText("Usuario:")
        user_label.setFont(QFont('Medio', 12))
        user_label.setStyleSheet("color:red;")
        user_label.move(20, 120)

        self.user_input = QLineEdit(self)
        self.user_input.resize(250, 24)
        self.user_input.move(90, 120)

        password_label = QLabel(self)
        password_label.setText("Password:")
        password_label.setFont(QFont('Medio', 12))
        password_label.setStyleSheet("color:red;")
        password_label.move(20, 160)

        self.password_input = QLineEdit(self)
        self.password_input.resize(250, 24)
        self.password_input.move(90, 160)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.iniciar_mainview)  # Conecta al método iniciar_mainview

        self.check_view_password = QCheckBox(self)
        self.check_view_password.setText("Ver Contraseña")
        self.check_view_password.move(100, 190)
        self.check_view_password.toggled.connect(self.mostrar_contrasena)

        login_button = QPushButton(self)
        login_button.setText("Ingresar")
        login_button.resize(100, 24)
        login_button.move(120, 250)
        login_button.clicked.connect(self.iniciar_mainview)


    def mostrar_contrasena(self, clicked):
        if clicked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)#Oculta la contraseña

    def iniciar_mainview(self):
        nombre_usuario = self.user_input.text()
        contraseña = self.password_input.text()

        usuario = UsuarioDAO.login(nombre_usuario, contraseña)
        if usuario:
            self.paginaprincipal(usuario.rol)  # Pasar el rol del usuario
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
            self.user_input.clear()
            self.password_input.clear()

    def paginaprincipal(self, rol):
        self.main_window = MainWindowPri(rol)  # Enviamos el rol al crear la instancia de MainWindowPri
        self.main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginR()
    sys.exit(app.exec())
