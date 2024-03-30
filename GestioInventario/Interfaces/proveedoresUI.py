import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QPixmap

class SupplierRegistrationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Proveedores")
        self.setGeometry(80, 55, 1200, 650)

        # Create input fields
        self.nombre_input = QLineEdit()
        self.apellido_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.email_input = QLineEdit()

        # Create labels
        self.nombre_label = QLabel("Nombre:")
        self.apellido_label = QLabel("Apellido:")
        self.direccion_label = QLabel("Dirección:")
        self.telefono_label = QLabel("Teléfono:")
        self.email_label = QLabel("Email:")

        # Load and display the image
        self.image_label = QLabel()
        pixmap = QPixmap("path/to/your/image.png")  # Replace with the actual path to your image
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Resize the image to fit the label

        # Create submit button
        self.submit_button = QPushButton("Registrar")

        # Set up layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.nombre_label)
        input_layout.addWidget(self.nombre_input)
        input_layout.addWidget(self.apellido_label)
        input_layout.addWidget(self.apellido_input)
        input_layout.addWidget(self.direccion_label)
        input_layout.addWidget(self.direccion_input)
        input_layout.addWidget(self.telefono_label)
        input_layout.addWidget(self.telefono_input)
        input_layout.addWidget(self.email_label)
        input_layout.addWidget(self.email_input)

        main_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.image_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SupplierRegistrationApp()
    window.show()
    sys.exit(app.exec())
