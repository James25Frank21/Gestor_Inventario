import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QWidget


class VentanaPrincipal(QMainWindow):
    def __init__(self, nombre_usuario):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        self.setGeometry(400, 200, 300, 200)

        self.layout = QVBoxLayout()

        self.input_label = QLineEdit()
        self.input_label.setPlaceholderText("Ingrese un valor:")
        self.layout.addWidget(self.input_label)

        self.boton_mostrar_valor = QPushButton("Mostrar Valor")
        self.boton_mostrar_valor.clicked.connect(self.mostrar_valor)
        self.layout.addWidget(self.boton_mostrar_valor)

        self.widget_central = QWidget()
        self.widget_central.setLayout(self.layout)
        self.setCentralWidget(self.widget_central)

        self.nombre_usuario = nombre_usuario

    def mostrar_valor(self):
        valor = self.input_label.text()
        if valor:
            print("El valor ingresado es:", valor)
            print("Usuario:", self.nombre_usuario)
        else:
            print("Ingrese un valor antes de presionar el botón.")


def main():
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal("")
    ventana_principal.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
