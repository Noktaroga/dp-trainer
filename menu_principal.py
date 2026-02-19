import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame)
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt

class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        
        # ==== CONFIG VENTANA ====
        self.setWindowTitle('DP-700 Training System - Matrix Edition')
        self.setMinimumSize(1000, 700)
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#000000'))
        palette.setColor(QPalette.WindowText, QColor('#00FF00'))
        self.setPalette(palette)
        
        font = QFont('Courier New', 13)
        self.setFont(font)
        
        # ==== LAYOUT PRINCIPAL ====
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # ── Header ──
        header_frame = QFrame()
        header_frame.setStyleSheet('''
            background: #0a0a0a;
            border: 2px solid #00FF00;
            border-radius: 5px;
            padding: 20px;
        ''')
        header_layout = QVBoxLayout()
        
        title_label = QLabel('DP-700 TRAINING SYSTEM')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('''
            color: #00FF00;
            font-size: 28px;
            font-weight: bold;
            font-family: Courier New, monospace;
        ''')
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel('Microsoft Fabric Data Engineer')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet('''
            color: #00DD00;
            font-size: 16px;
            font-family: Courier New, monospace;
        ''')
        header_layout.addWidget(subtitle_label)
        
        ascii_art = QLabel('''
        █▀▄▀█ ▄▀█ ▀█▀ █▀█ █ ▀▄▀   █▀▀ █▀▄ █ ▀█▀ █ █▀█ █▄ █
        █ ▀ █ █▀█  █  █▀▄ █ █ █   ██▄ █▄▀ █  █  █ █▄█ █ ▀█
        ''')
        ascii_art.setAlignment(Qt.AlignCenter)
        ascii_art.setStyleSheet('''
            color: #00FF00;
            font-size: 11px;
            font-family: Courier New, monospace;
        ''')
        header_layout.addWidget(ascii_art)
        
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)
        
        # ── Instrucciones ──
        instructions = QLabel('SELECCIONA TU MODO DE ENTRENAMIENTO:')
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet('''
            color: #FFFF00;
            font-size: 16px;
            font-weight: bold;
            font-family: Courier New, monospace;
            padding: 15px;
        ''')
        layout.addWidget(instructions)
        
        # ── Botón Modo Comandos ──
        btn_comandos = QPushButton('► MODO COMANDOS')
        btn_comandos.setFixedHeight(120)
        btn_comandos.setStyleSheet('''
            QPushButton {
                color: #00FF00;
                background: #0a0a0a;
                border: 3px solid #00FF00;
                border-radius: 5px;
                font-size: 22px;
                font-weight: bold;
                font-family: Courier New, monospace;
                padding: 15px;
            }
            QPushButton:hover {
                background: #00FF00;
                color: #000000;
            }
            QPushButton:pressed {
                background: #00DD00;
            }
        ''')
        btn_comandos.clicked.connect(self.launch_matrix_trainer)
        layout.addWidget(btn_comandos)
        
        desc_comandos = QLabel('Entrenamiento paso a paso de comandos SQL y scripts.\nPerfecto para memorizar sintaxis y estructuras.')
        desc_comandos.setAlignment(Qt.AlignCenter)
        desc_comandos.setStyleSheet('''
            color: #00DD00;
            font-size: 13px;
            font-family: Courier New, monospace;
        ''')
        layout.addWidget(desc_comandos)
        
        # ── Botón Modo Estudio ──
        btn_estudio = QPushButton('► MODO ESTUDIO DE MÓDULOS')
        btn_estudio.setFixedHeight(120)
        btn_estudio.setStyleSheet('''
            QPushButton {
                color: #FFFF00;
                background: #0a0a0a;
                border: 3px solid #FFFF00;
                border-radius: 5px;
                font-size: 22px;
                font-weight: bold;
                font-family: Courier New, monospace;
                padding: 15px;
            }
            QPushButton:hover {
                background: #FFFF00;
                color: #000000;
            }
            QPushButton:pressed {
                background: #DDDD00;
            }
        ''')
        btn_estudio.clicked.connect(self.launch_estudio_modulos)
        layout.addWidget(btn_estudio)
        
        desc_estudio = QLabel('Sistema de preguntas por módulos con modos de refuerzo.\nIdeal para preparación conceptual y certificación.')
        desc_estudio.setAlignment(Qt.AlignCenter)
        desc_estudio.setStyleSheet('''
            color: #DDDD00;
            font-size: 13px;
            font-family: Courier New, monospace;
        ''')
        layout.addWidget(desc_estudio)
        
        layout.addStretch()
        
        # ── Footer ──
        footer = QLabel('© 2026 - Presiona ESC para salir')
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet('''
            color: #006600;
            font-size: 11px;
            font-family: Courier New, monospace;
        ''')
        layout.addWidget(footer)
        
        self.setLayout(layout)
    
    def launch_matrix_trainer(self):
        """Ejecuta el Matrix Trainer (modo comandos)"""
        try:
            subprocess.Popen([sys.executable, 'matrix_trainer.py'])
        except Exception as e:
            print(f"Error al lanzar Matrix Trainer: {e}")
    
    def launch_estudio_modulos(self):
        """Ejecuta el sistema de estudio de módulos"""
        try:
            subprocess.Popen([sys.executable, 'estudio_modulos.py'])
        except Exception as e:
            print(f"Error al lanzar Estudio de Módulos: {e}")
    
    def keyPressEvent(self, event):
        """Permite cerrar con ESC"""
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MenuPrincipal()
    # Centrar la ventana en la pantalla
    screen = app.primaryScreen().geometry()
    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2
    window.move(x, y)
    window.show()
    sys.exit(app.exec_())
