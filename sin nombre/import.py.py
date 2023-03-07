import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout


class App(QWidget):
    def __init__(self):
        super().__init__()
        
        # Conectar a la base de datos
        self.conn = sqlite3.connect('hospital.db')
        self.cur = self.conn.cursor()

        # Crear la tabla "usuarios" si no existe
        self.cur.execute('''CREATE TABLE IF NOT EXISTS usuarios
                            (correo TEXT PRIMARY KEY,
                            contrasena TEXT)''')
        self.conn.commit()

        # Agregar un usuario de ejemplo
        self.agregar_usuario("los@gmail.com", "MINI")
        
        # Crear formulario de ingreso de pacientes
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        self.form_widget.hide()

        # Crear tabla de pacientes
        self.cur.execute('''CREATE TABLE IF NOT EXISTS pacientes
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        apellido TEXT,
                        telefono TEXT,
                        fecha TEXT,
                        hora TEXT)''')
        self.conn.commit()

        # Crear widgets
        self.lbl_correo = QLabel('Correo electrónico:')
        self.txt_correo = QLineEdit()
        self.lbl_contrasena = QLabel('Contraseña:')
        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setEchoMode(QLineEdit.Password)
        self.btn_iniciar_sesion = QPushButton('Iniciar sesión')
        self.btn_agregar = QPushButton('Agregar')
        self.txt_registro = QTextEdit()
        self.txt_nombre = QLineEdit()
        self.txt_apellido = QLineEdit()
        self.txt_telefono = QLineEdit()
        self.txt_fecha = QLineEdit()
        self.txt_hora = QLineEdit()

        # Ocultar formulario de ingreso de pacientes hasta que se inicie sesión
    def cerrar_ventana(self):
        if hasattr(self, 'ventana'):
             self.ventana.close()
        self.form_layout.addWidget(QLabel('Nombre:'))
        self.form_layout.addWidget(self.txt_nombre)
        self.form_layout.addWidget(QLabel('Apellido:'))
        self.form_layout.addWidget(self.txt_apellido)
        self.form_layout.addWidget(QLabel('Teléfono:'))
        self.form_layout.addWidget(self.txt_telefono)
        self.form_layout.addWidget(QLabel('Fecha:'))
        self.form_layout.addWidget(self.txt_fecha)
        self.form_layout.addWidget(QLabel('Hora:'))
        self.form_layout.addWidget(self.txt_hora)
        self.form_layout.addWidget(self.btn_agregar)
        self.form_layout.addWidget(self.txt_registro)
        self.setLayout(self.form_layout)
        self.show()
        self.form_widget.hide()

        # Conectar eventos
        self.btn_iniciar_sesion.clicked.connect(self.iniciar_sesion)
        self.btn_agregar.clicked.connect(self.agregar_registro)
        
        # Crear layout
        
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_correo)
        layout.addWidget(self.txt_correo)
        layout.addWidget(self.lbl_contrasena)
        layout.addWidget(self.txt_contrasena)
        layout.addWidget(self.btn_iniciar_sesion)
        layout.addStretch(1)
        layout.addWidget(self.form_widget)

        # Agrega el widget de inicio de sesión al layout principal
        layout.addWidget(self.widget_de_inicio_de_sesion)

    def agregar_usuario(self, correo, contrasena):
        self.cur.execute("INSERT OR IGNORE INTO usuarios (correo, contrasena) VALUES (?, ?)",
                         (correo, contrasena))
        self.conn.commit()

    def iniciar_sesion(self):
        self.widget_de_inicio_de_sesion = QWidget()
        correo = self.txt_correo.text()
        contrasena = self.txt_contrasena.text()
        

        # Verificar que las credenciales sean válidas
        self.cur.execute(
            "SELECT * FROM usuarios WHERE correo=? AND contrasena=?", (correo, contrasena))
        (correo, contrasena)
        usuario = self.cur.fetchone()
        if usuario is not None:
            # Si las credenciales son válidas, abrir una nueva ventana y mostrar el formulario
             self.ventana = QWidget()
             self.ventana.setWindowTitle('Ingreso de pacientes')
             self.ventana.setGeometry(100, 100, 400, 300)
             self.ventana.setLayout(self.form_layout)
             self.ventana.show()

        else:
            # Si las credenciales no son válidas, mostrar un mensaje de error
             self.btn_agregar.setEnabled(False)
             self.txt_registro.setText('Credenciales inválidas.')

    def agregar_registro(self):
        # Obtener los valores de los campos de entrada
        nombre = self.txt_nombre.text()
        apellido = self.txt_apellido.text()
        telefono = self.txt_telefono.text()
        fecha = self.txt_fecha.text()
        hora = self.txt_hora.text()

        # Insertar los valores en la tabla "pacientes"
        self.cur.execute("INSERT INTO pacientes (nombre, apellido, telefono, fecha, hora) VALUES (?, ?, ?, ?, ?)",
                         (nombre, apellido, telefono, fecha, hora))
        self.conn.commit()

        # Limpiar los campos de entrada y mostrar un mensaje de confirmación
        self.txt_nombre.clear()
        self.txt_apellido.clear()
        self.txt_telefono.clear()
        self.txt_fecha.clear()
        self.txt_hora.clear()
        self.txt_registro.setText('Registro agregado correctamente.')


if __name__ == '__main__':
    # Crear aplicación
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
