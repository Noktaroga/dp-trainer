"""
Matrix Command Trainer v2.0 - Experiencia de Consola SQL Real
Modo de entrenamiento que simula una consola SQL real con:
- Syntax highlighting en tiempo real
- Autocompletado inteligente
- Validación completa del comando
- Historial de comandos
- Modo libre vs modo guiado
"""

import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QProgressBar, QMessageBox, QFrame,
    QCompleter, QSplitter, QTabWidget, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QColor, QPalette, QFont, QTextCursor, QKeySequence
from PyQt5.QtCore import Qt, QStringListModel, pyqtSignal, QTimer
from sql_syntax_highlighter import SQLSyntaxHighlighter
from stats_manager import StatsManager


class SQLConsoleWidget(QTextEdit):
    """Widget de consola SQL con características avanzadas"""
    
    executeCommand = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.command_history = []
        self.history_index = -1
        self.setFont(QFont('Consolas', 12))
        self.setStyleSheet('''
            QTextEdit {
                background: #0a0a0a;
                color: #00FF00;
                border: 2px solid #00FF00;
                border-radius: 5px;
                padding: 10px;
                selection-background-color: #003300;
            }
        ''')
        
        # Configurar autocompletado
        self.completer = None
        self.setup_completer()
    
    def setup_completer(self):
        """Configura el autocompletado SQL"""
        sql_keywords = [
            'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'DELETE',
            'CREATE', 'TABLE', 'ALTER', 'DROP', 'INDEX', 'VIEW', 'JOIN', 'INNER',
            'LEFT', 'RIGHT', 'OUTER', 'ON', 'AND', 'OR', 'NOT', 'NULL', 'IS',
            'LIKE', 'IN', 'BETWEEN', 'EXISTS', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
            'GROUP BY', 'HAVING', 'ORDER BY', 'ASC', 'DESC', 'LIMIT', 'OFFSET',
            'UNION', 'ALL', 'DISTINCT', 'AS', 'WITH', 'PRIMARY KEY', 'FOREIGN KEY',
            'REFERENCES', 'CONSTRAINT', 'UNIQUE', 'CHECK', 'DEFAULT',
            'BIGINT', 'INT', 'VARCHAR', 'CHAR', 'TEXT', 'DECIMAL', 'FLOAT',
            'DATE', 'TIME', 'DATETIME', 'DATETIME2', 'TIMESTAMP', 'BOOLEAN', 'BIT',
            'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'UPPER', 'LOWER', 'LEN',
            'SUBSTRING', 'REPLACE', 'CONCAT', 'COALESCE', 'CAST', 'CONVERT',
            'ROW_NUMBER', 'RANK', 'DENSE_RANK'
        ]
        
        self.completer = QCompleter(sql_keywords, self)
        self.completer.setWidget(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)
    
    def insert_completion(self, completion):
        """Inserta el texto autocompletado"""
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
    
    def keyPressEvent(self, event):
        """Maneja eventos de teclado para autocompletado e historial"""
        # F5 o Ctrl+Enter para ejecutar
        if event.key() == Qt.Key_F5 or (event.key() == Qt.Key_Return and 
                                        event.modifiers() == Qt.ControlModifier):
            self.execute_current_command()
            return
        
        # Flecha arriba/abajo para navegar historial
        if event.key() == Qt.Key_Up and event.modifiers() == Qt.ControlModifier:
            self.navigate_history(-1)
            return
        elif event.key() == Qt.Key_Down and event.modifiers() == Qt.ControlModifier:
            self.navigate_history(1)
            return
        
        # Ctrl+Space para autocompletado
        if event.key() == Qt.Key_Space and event.modifiers() == Qt.ControlModifier:
            self.show_completer()
            return
        
        super().keyPressEvent(event)
        
        # Mostrar autocompletado automático
        if event.text().isalpha():
            self.show_completer()
    
    def show_completer(self):
        """Muestra el autocompletado"""
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        prefix = tc.selectedText()
        
        if len(prefix) < 2:
            return
        
        self.completer.setCompletionPrefix(prefix)
        popup = self.completer.popup()
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
        
        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + 
                   self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)
    
    def execute_current_command(self):
        """Ejecuta el comando actual"""
        command = self.toPlainText().strip()
        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            self.executeCommand.emit(command)
    
    def navigate_history(self, direction):
        """Navega por el historial de comandos"""
        if not self.command_history:
            return
        
        self.history_index += direction
        self.history_index = max(0, min(self.history_index, len(self.command_history)))
        
        if self.history_index < len(self.command_history):
            self.setPlainText(self.command_history[self.history_index])
        else:
            self.clear()


class MatrixTrainerV2(QWidget):
    """Matrix Command Trainer v2 - Experiencia de Consola SQL Real"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializar gestor de estadísticas
        self.stats_manager = StatsManager()
        self.session_id = self.stats_manager.start_session('matrix_trainer_v2')
        self.session_start = datetime.now()
        
        # Estado del trainer
        self.xml_files = sorted([f for f in os.listdir('.') if f.startswith('command_') and f.endswith('.xml')])
        self.current_file_index = 0
        self.current_command = None
        self.mode = 'guided'  # 'guided' o 'free'
        self.attempts = 0
        self.command_start_time = None
        
        self.setup_ui()
        self.load_command()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.setWindowTitle('Matrix SQL Console - Training Mode v2.0')
        
        # Paleta de colores Matrix
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#000000'))
        palette.setColor(QPalette.WindowText, QColor('#00FF00'))
        self.setPalette(palette)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # === HEADER ===
        header = self.create_header()
        main_layout.addWidget(header)
        
        # === SPLITTER: Info + Console ===
        splitter = QSplitter(Qt.Vertical)
        
        # Panel de información del comando
        info_widget = self.create_info_panel()
        splitter.addWidget(info_widget)
        
        # Consola SQL
        console_widget = self.create_console_panel()
        splitter.addWidget(console_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter, stretch=1)
        
        # === FOOTER ===
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
    
    def create_header(self):
        """Crea el header con progreso global"""
        header = QFrame()
        header.setStyleSheet('''
            QFrame {
                background: #0a0a0a;
                border: 2px solid #00FF00;
                border-radius: 8px;
                padding: 15px;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel('⚡ MATRIX SQL CONSOLE - TRAINING MODE ⚡')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('''
            color: #00FF00;
            font-size: 22px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        ''')
        layout.addWidget(title)
        
        # Progreso
        progress_layout = QHBoxLayout()
        
        self.progress_label = QLabel()
        self.progress_label.setStyleSheet('color: #00DD00; font-size: 13px;')
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setStyleSheet('''
            QProgressBar {
                border: 1px solid #004000;
                background: #0a0a0a;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #00FF00, stop:1 #00DD00);
                border-radius: 5px;
            }
        ''')
        progress_layout.addWidget(self.progress_bar, stretch=1)
        
        layout.addLayout(progress_layout)
        
        header.setLayout(layout)
        return header
    
    def create_info_panel(self):
        """Crea el panel de información del comando"""
        info_frame = QFrame()
        info_frame.setStyleSheet('''
            QFrame {
                background: #050505;
                border: 1px solid #003300;
                border-radius: 5px;
                padding: 10px;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Tabs para diferentes vistas
        self.info_tabs = QTabWidget()
        self.info_tabs.setStyleSheet('''
            QTabWidget::pane {
                border: 1px solid #003300;
                background: #0a0a0a;
            }
            QTabBar::tab {
                background: #0a0a0a;
                color: #00DD00;
                padding: 8px 20px;
                border: 1px solid #003300;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #001a00;
                color: #00FF00;
                border-bottom: 2px solid #00FF00;
            }
        ''')
        
        # Tab 1: Objetivo
        objective_widget = QWidget()
        obj_layout = QVBoxLayout()
        
        self.title_label = QLabel()
        self.title_label.setStyleSheet('''
            color: #00FF00;
            font-size: 16px;
            font-weight: bold;
            padding: 5px;
        ''')
        self.title_label.setWordWrap(True)
        obj_layout.addWidget(self.title_label)
        
        self.desc_label = QLabel()
        self.desc_label.setStyleSheet('''
            color: #00DD00;
            font-size: 13px;
            padding: 5px;
        ''')
        self.desc_label.setWordWrap(True)
        obj_layout.addWidget(self.desc_label)
        
        obj_layout.addStretch()
        objective_widget.setLayout(obj_layout)
        
        # Tab 2: Pistas
        hints_widget = QWidget()
        hints_layout = QVBoxLayout()
        
        self.hints_list = QListWidget()
        self.hints_list.setStyleSheet('''
            QListWidget {
                background: #0a0a0a;
                color: #FFFF99;
                border: none;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-left: 3px solid #FFFF00;
                margin: 5px;
                background: #131300;
            }
        ''')
        hints_layout.addWidget(self.hints_list)
        hints_widget.setLayout(hints_layout)
        
        # Tab 3: Solución (oculta inicialmente)
        solution_widget = QWidget()
        sol_layout = QVBoxLayout()
        
        self.solution_label = QLabel()
        self.solution_label.setStyleSheet('''
            background: #001a00;
            color: #00FF00;
            padding: 15px;
            border: 1px solid #003300;
            border-radius: 5px;
            font-size: 13px;
            font-family: 'Consolas', monospace;
        ''')
        self.solution_label.setWordWrap(True)
        self.solution_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        sol_layout.addWidget(self.solution_label)
        
        solution_widget.setLayout(sol_layout)
        
        self.info_tabs.addTab(objective_widget, '🎯 Objetivo')
        self.info_tabs.addTab(hints_widget, '💡 Pistas')
        self.info_tabs.addTab(solution_widget, '🔍 Solución')
        
        layout.addWidget(self.info_tabs)
        info_frame.setLayout(layout)
        return info_frame
    
    def create_console_panel(self):
        """Crea el panel de consola SQL"""
        console_frame = QFrame()
        console_frame.setStyleSheet('''
            QFrame {
                background: #050505;
                border: 1px solid #003300;
                border-radius: 5px;
                padding: 10px;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Header de la consola
        console_header = QLabel('📟 SQL CONSOLE - [WRITE MODE]')
        console_header.setStyleSheet('''
            color: #00FF00;
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
        ''')
        layout.addWidget(console_header)
        
        # Editor SQL
        self.sql_editor = SQLConsoleWidget()
        self.sql_highlighter = SQLSyntaxHighlighter(self.sql_editor.document(), theme='matrix')
        self.sql_editor.executeCommand.connect(self.validate_command)
        layout.addWidget(self.sql_editor, stretch=1)
        
        # Ayuda rápida
        help_text = QLabel('💻 F5 o Ctrl+Enter: Ejecutar | Ctrl+↑/↓: Historial | Ctrl+Space: Autocompletar')
        help_text.setStyleSheet('''
            color: #006600;
            font-size: 11px;
            padding: 5px;
            font-style: italic;
        ''')
        layout.addWidget(help_text)
        
        console_frame.setLayout(layout)
        return console_frame
    
    def create_footer(self):
        """Crea el footer con controles"""
        footer = QFrame()
        footer.setStyleSheet('''
            QFrame {
                background: #0a0a0a;
                border: 1px solid #003300;
                border-radius: 5px;
                padding: 10px;
            }
        ''')
        
        layout = QHBoxLayout()
        
        # Estado
        self.status_label = QLabel()
        self.status_label.setStyleSheet('''
            color: #00FF00;
            font-size: 12px;
            padding: 5px;
        ''')
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Botón modo
        self.mode_btn = QPushButton('🎮 Modo: GUIADO')
        self.mode_btn.setStyleSheet('''
            QPushButton {
                background: #0a0a0a;
                color: #FFFF00;
                border: 2px solid #FFFF00;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #FFFF00;
                color: #000000;
            }
        ''')
        self.mode_btn.clicked.connect(self.toggle_mode)
        layout.addWidget(self.mode_btn)
        
        # Botón validar
        self.validate_btn = QPushButton('✓ EJECUTAR (F5)')
        self.validate_btn.setStyleSheet('''
            QPushButton {
                background: #0a0a0a;
                color: #00FF00;
                border: 2px solid #00FF00;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00FF00;
                color: #000000;
            }
        ''')
        self.validate_btn.clicked.connect(lambda: self.validate_command(self.sql_editor.toPlainText()))
        layout.addWidget(self.validate_btn)
        
        # Botón siguiente
        self.next_btn = QPushButton('► SIGUIENTE')
        self.next_btn.setStyleSheet('''
            QPushButton {
                background: #0a0a0a;
                color: #00DD00;
                border: 2px solid #00DD00;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00DD00;
                color: #000000;
            }
        ''')
        self.next_btn.clicked.connect(self.next_command)
        self.next_btn.hide()
        layout.addWidget(self.next_btn)
        
        footer.setLayout(layout)
        return footer
    
    def load_command(self):
        """Carga el comando actual desde XML"""
        if self.current_file_index >= len(self.xml_files):
            self.finish_training()
            return
        
        # Cargar datos del comando
        filename = self.xml_files[self.current_file_index]
        tree = ET.parse(filename)
        root = tree.getroot()
        
        self.current_command = {
            'filename': filename,
            'title': root.findtext('title', default=''),
            'description': root.findtext('description', default=''),
            'parts': [part.findtext('text', default='') for part in root.find('parts').findall('part')],
            'descriptions': [part.findtext('desc', default='') for part in root.find('parts').findall('part')],
            'full': root.findtext('full', default='')
        }
        
        # Reiniciar estado
        self.attempts = 0
        self.command_start_time = datetime.now()
        self.sql_editor.clear()
        self.sql_editor.setFocus()
        self.next_btn.hide()
        
        # Actualizar UI
        self.update_progress()
        self.title_label.setText(f"📋 {self.current_command['title']}")
        self.desc_label.setText(self.current_command['description'])
        
        # Actualizar pistas
        self.hints_list.clear()
        for i, (part, desc) in enumerate(zip(self.current_command['parts'], 
                                              self.current_command['descriptions']), 1):
            item = QListWidgetItem(f"{i}. {desc}")
            self.hints_list.addItem(item)
        
        # Actualizar solución (oculta al inicio)
        self.solution_label.setText(self.current_command['full'])
        
        self.status_label.setText('⚡ Escribe el comando SQL y presiona F5 para validar')
    
    def update_progress(self):
        """Actualiza la barra de progreso"""
        current = self.current_file_index + 1
        total = len(self.xml_files)
        progress = int((self.current_file_index / total) * 100) if total > 0 else 0
        
        self.progress_label.setText(f'Comando {current} de {total}')
        self.progress_bar.setValue(progress)
    
    def toggle_mode(self):
        """Cambia entre modo guiado y modo libre"""
        if self.mode == 'guided':
            self.mode = 'free'
            self.mode_btn.setText('🎮 Modo: LIBRE')
            self.mode_btn.setStyleSheet(self.mode_btn.styleSheet().replace('#FFFF00', '#00FFFF'))
        else:
            self.mode = 'guided'
            self.mode_btn.setText('🎮 Modo: GUIADO')
            self.mode_btn.setStyleSheet(self.mode_btn.styleSheet().replace('#00FFFF', '#FFFF00'))
    
    def validate_command(self, user_command):
        """Valida el comando ingresado por el usuario"""
        user_command = user_command.strip()
        expected_command = self.current_command['full'].strip()
        
        self.attempts += 1
        
        # Normalizar para comparación (eliminar espacios extras y convertir a mayúsculas)
        def normalize(cmd):
            return ' '.join(cmd.upper().split())
        
        user_normalized = normalize(user_command)
        expected_normalized = normalize(expected_command)
        
        if user_normalized == expected_normalized:
            # ¡Correcto!
            elapsed_time = (datetime.now() - self.command_start_time).total_seconds()
            
            # Registrar en estadísticas
            self.stats_manager.record_matrix_command(
                command_name=self.current_command['title'],
                attempts=self.attempts,
                errors=self.attempts - 1,
                time_seconds=elapsed_time,
                completed=True
            )
            
            # Mostrar éxito
            self.show_success(elapsed_time)
            self.sql_editor.setDisabled(True)
            self.validate_btn.hide()
            self.next_btn.show()
            
        else:
            # Incorrecto
            if self.mode == 'guided':
                self.show_hints(user_normalized, expected_normalized)
            else:
                self.status_label.setText(f'❌ Intento {self.attempts}: Comando incorrecto. Revisa la sintaxis.')
    
    def show_success(self, elapsed_time):
        """Muestra mensaje de éxito"""
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
        
        msg = f'✅ ¡CORRECTO! Completado en {time_str} con {self.attempts} intento(s)'
        self.status_label.setText(msg)
        self.status_label.setStyleSheet('color: #00FF00; font-size: 14px; font-weight: bold; padding: 5px;')
        
        # Animación de éxito
        QTimer.singleShot(200, lambda: self.sql_editor.setStyleSheet(
            self.sql_editor.styleSheet().replace('border: 2px solid #00FF00', 
                                                  'border: 3px solid #00FF00')))
    
    def show_hints(self, user_cmd, expected_cmd):
        """Muestra pistas comparando el comando del usuario con el esperado"""
        user_words = user_cmd.split()
        expected_words = expected_cmd.split()
        
        # Encontrar primera diferencia
        for i, (u_word, e_word) in enumerate(zip(user_words, expected_words)):
            if u_word != e_word:
                hint = f'⚠️ Revisa la palabra #{i+1}: Esperado "{e_word}", recibido "{u_word}"'
                self.status_label.setText(hint)
                return
        
        # Diferencia en longitud
        if len(user_words) != len(expected_words):
            hint = f'⚠️ Comando tiene {len(user_words)} palabras, se esperan {len(expected_words)}'
            self.status_label.setText(hint)
        else:
            self.status_label.setText('⚠️ Comando incorrecto. Revisa mayúsculas/minúsculas o espaciado.')
    
    def next_command(self):
        """Avanza al siguiente comando"""
        self.current_file_index += 1
        self.sql_editor.setDisabled(False)
        self.validate_btn.show()
        self.load_command()
    
    def finish_training(self):
        """Finaliza la sesión de entrenamiento"""
        # Guardar estadísticas de sesión
        session_duration = (datetime.now() - self.session_start).total_seconds() / 60
        self.stats_manager.end_session(self.session_id, {
            'commands_completed': self.current_file_index,
            'total_commands': len(self.xml_files)
        })
        
        self.progress_label.setText(f'Completado: {len(self.xml_files)}/{len(self.xml_files)}')
        self.progress_bar.setValue(100)
        self.title_label.setText('🏆 ¡ENTRENAMIENTO COMPLETADO!')
        self.desc_label.setText('Has practicado todos los comandos SQL disponibles.')
        self.status_label.setText(f'Sesión finalizada - Duración: {int(session_duration)} minutos')
        self.sql_editor.setDisabled(True)
        self.validate_btn.hide()
        self.next_btn.hide()
        self.hints_list.clear()
    
    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        # Guardar progreso antes de cerrar
        if self.current_file_index < len(self.xml_files):
            session_duration = (datetime.now() - self.session_start).total_seconds() / 60
            self.stats_manager.end_session(self.session_id, {
                'commands_completed': self.current_file_index,
                'total_commands': len(self.xml_files),
                'interrupted': True
            })
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MatrixTrainerV2()
    window.showMaximized()
    sys.exit(app.exec_())
