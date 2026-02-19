import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QProgressBar
)
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET
import os


class CommandTrainer(QWidget):
    def __init__(self):
        super().__init__()

        # ==== CONFIG VENTANA ====
        self.setWindowTitle('Matrix Command Trainer - DP700')
        # Ventana maximizada para aprovechar toda la pantalla

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#050505'))
        palette.setColor(QPalette.WindowText, QColor('#00FF00'))
        self.setPalette(palette)

        font = QFont('Courier New', 12)
        self.setFont(font)

        # ==== ESTADO ====
        self.xml_files = [f for f in os.listdir('.') if f.startswith('command_') and f.endswith('.xml')]
        self.xml_files.sort()
        self.current_file = 0
        self.errors = 0
        self.max_errors = 3
        self.parts = []
        self.descriptions = []

        # ==== LAYOUT PRINCIPAL ====
        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        # ── Fila superior: progreso global ──
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        self.progress_label = QLabel()
        self.progress_label.setStyleSheet('color: #00FF00; font-size: 12px; font-weight: bold;')
        top_layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setStyleSheet('''
            QProgressBar {
                border: 1px solid #004000;
                background: #101010;
            }
            QProgressBar::chunk {
                background: #00FF00;
            }
        ''')
        top_layout.addWidget(self.progress_bar)

        layout.addLayout(top_layout)

        # ── Título y objetivo ──
        self.title_label = QLabel()
        self.title_label.setStyleSheet('color: #00FF41; font-size: 14px; font-weight: bold;')
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)

        self.desc_label = QLabel()
        self.desc_label.setStyleSheet('color: #00DD00; font-size: 12px;')
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)

        # ── Comando visual ──
        code_header = QLabel('COMANDO:')
        code_header.setStyleSheet('color: #00FF00; font-size: 12px; font-weight: bold;')
        layout.addWidget(code_header)

        self.code_label = QLabel()
        self.code_label.setStyleSheet('''
            background: #000;
            color: #00FF00;
            padding: 10px;
            border: 1px solid #003300;
            border-radius: 2px;
            font-size: 12px;
        ''')
        self.code_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.code_label.setWordWrap(True)
        layout.addWidget(self.code_label)

        # ── Pista ──
        self.hint_label = QLabel()
        self.hint_label.setStyleSheet('''
            color: #FFFF99;
            background: #131300;
            border-left: 3px solid #FFFF00;
            padding: 6px 10px;
            font-size: 11px;
        ''')
        self.hint_label.setWordWrap(True)
        layout.addWidget(self.hint_label)

        # ── Input + progreso de partes ──
        self.part_progress_label = QLabel()
        self.part_progress_label.setStyleSheet('color: #00FF00; font-size: 11px;')
        layout.addWidget(self.part_progress_label)

        self.input = QLineEdit()
        self.input.setStyleSheet('''
            QLineEdit {
                color: #00FF00;
                background: #101010;
                border: 2px solid #00FF00;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #FFFF00;
            }
        ''')
        self.input.setPlaceholderText('Escribe la siguiente parte y presiona ENTER...')
        layout.addWidget(self.input)

        # ── Barra inferior: estado + errores + botón siguiente ──
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(12)

        self.status_label = QLabel()
        self.status_label.setStyleSheet('color: #00FF00; font-size: 11px;')
        bottom_layout.addWidget(self.status_label)

        self.error_label = QLabel()
        self.error_label.setStyleSheet('color: #FF5555; font-size: 11px; font-weight: bold;')
        bottom_layout.addWidget(self.error_label)

        bottom_layout.addStretch()

        self.next_btn = QPushButton('Siguiente ►')
        self.next_btn.setStyleSheet('''
            QPushButton {
                color: #00FF00;
                background: #101010;
                border: 1px solid #00FF00;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #00FF00;
                color: #000;
            }
        ''')
        self.next_btn.clicked.connect(self.next_command)
        self.next_btn.hide()
        bottom_layout.addWidget(self.next_btn)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        # Eventos
        self.input.returnPressed.connect(self.check_word)

        # Cargar primer comando
        self.load_command()

    # ==== LÓGICA ====
    def load_command_from_xml(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        title = root.findtext('title', default='')
        description = root.findtext('description', default='')
        parts = []
        descs = []
        for part in root.find('parts').findall('part'):
            parts.append(part.findtext('text', default=''))
            descs.append(part.findtext('desc', default=''))
        full = root.findtext('full', default='')
        return {'title': title, 'description': description, 'parts': parts, 'descs': descs, 'full': full}

    def load_command(self):
        if self.current_file >= len(self.xml_files):
            self.progress_label.setText(f'Completado: {len(self.xml_files)}/{len(self.xml_files)} comandos')
            self.progress_bar.setValue(100)
            self.title_label.setText('ENTRENAMIENTO COMPLETADO')
            self.desc_label.setText('Has practicado todos los comandos configurados.')
            self.code_label.setText('¡Listo para la certificación!')
            self.input.setDisabled(True)
            self.hint_label.clear()
            self.status_label.setText('Sesión finalizada')
            self.error_label.clear()
            self.part_progress_label.clear()
            self.next_btn.hide()
            return

        self.command_data = self.load_command_from_xml(self.xml_files[self.current_file])
        self.errors = 0
        self.parts = self.command_data['parts']
        self.descriptions = self.command_data['descs']
        self.part_index = 0
        self.input.clear()
        self.input.setDisabled(False)
        self.input.setFocus()

        # Progreso global
        progress = int((self.current_file / len(self.xml_files)) * 100) if self.xml_files else 0
        self.progress_label.setText(f'Comando {self.current_file + 1} de {len(self.xml_files)}')
        self.progress_bar.setValue(progress)

        self.title_label.setText(self.command_data['title'])
        self.desc_label.setText(self.command_data['description'])

        self.update_code_label()
        self.update_hint_label()
        self.update_part_progress()
        self.update_error_display()

        self.next_btn.hide()
        self.status_label.setText('Escribe la siguiente parte y presiona ENTER')

    def update_hint_label(self):
        if self.part_index < len(self.descriptions):
            self.hint_label.setText(f'Pista: {self.descriptions[self.part_index]}')
        else:
            self.hint_label.clear()

    def update_part_progress(self):
        total = len(self.parts)
        completed = self.part_index
        percentage = int((completed / total) * 100) if total else 0
        bar = '█' * completed + '░' * (total - completed)
        self.part_progress_label.setText(f'Partes: [{bar}] {completed}/{total} ({percentage}%)')

    def update_error_display(self):
        if self.errors == 0:
            self.error_label.clear()
        else:
            icons = '✗' * self.errors + '○' * (self.max_errors - self.errors)
            self.error_label.setText(f'Errores: [{icons}] {self.errors}/{self.max_errors}')

    def update_code_label(self):
        html = '<span style="font-family:Courier New,monospace; font-size:12px;">'
        for i, part in enumerate(self.parts):
            if i < self.part_index:
                html += (
                    '<span style="color:#00FF00; background:#102810; '
                    'padding:2px 6px; border-radius:2px; font-weight:bold;">'
                    f'{part}</span> '
                )
            elif i == self.part_index:
                html += (
                    '<span style="color:#FFFF00; background:#151500; '
                    'padding:2px 6px; border-radius:2px;">'
                    f'{"_" * len(part)}</span> '
                )
            else:
                html += (
                    '<span style="color:#003300; background:#000; '
                    'padding:2px 6px; border-radius:2px;">'
                    f'{"░" * len(part)}</span> '
                )
        html += '</span>'
        self.code_label.setText(html)

    def check_word(self):
        if not self.parts:
            return

        text = self.input.text().strip()
        expected = self.parts[self.part_index]

        if text == expected:
            self.part_index += 1
            self.input.clear()
            self.update_code_label()
            self.update_hint_label()
            self.update_part_progress()

            if self.part_index >= len(self.parts):
                self.status_label.setText('Comando completado.')
                self.input.setDisabled(True)
                html = (
                    '<span style="color:#00FF00; background:#102810; '
                    'font-family:Courier New,monospace; font-size:12px; '
                    'font-weight:bold; padding:6px; border-radius:2px;">'
                    f'{self.command_data["full"]}</span>'
                )
                self.code_label.setText(html)
                self.hint_label.setText('Pulsa "Siguiente" para continuar.')
                self.next_btn.show()
            else:
                self.status_label.setText(f'Correcto. Siguiente parte ({self.part_index + 1}/{len(self.parts)}).')
                self.input.setFocus()
        else:
            self.errors += 1
            self.update_error_display()
            self.status_label.setText('Incorrecto. Intenta de nuevo.')
            self.input.clear()
            self.input.setFocus()

            if self.errors >= self.max_errors:
                QMessageBox.warning(
                    self,
                    'Reinicio',
                    f'Demasiados errores ({self.max_errors}).\n\nEl comando se reiniciará.'
                )
                self.load_command()

    def next_command(self):
        self.current_file += 1
        self.load_command()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CommandTrainer()
    window.showMaximized()  # Ventana maximizada ocupando toda la pantalla
    sys.exit(app.exec_())
