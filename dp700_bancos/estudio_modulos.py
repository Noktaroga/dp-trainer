import sys
import csv
import os
import random
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QRadioButton, QButtonGroup, QFrame, QScrollArea,
    QComboBox, QMessageBox, QProgressBar, QDialog, QTableWidget, 
    QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QColor, QPalette, QFont, QCursor
from PyQt5.QtCore import Qt
from stats_manager import StatsManager

class ClickableLabel(QLabel):
    """Label clickeable que puede emitir eventos al hacer clic"""
    def __init__(self, text, callback, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.callback = callback
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(self.styleSheet() + '''
            QLabel:hover {
                background: #1a1a1a;
                transform: scale(1.05);
            }
        ''')
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.callback()
        super().mousePressEvent(event)

class QuestionDetailsDialog(QDialog):
    """Diálogo para mostrar detalles de preguntas filtradas"""
    def __init__(self, title, questions, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Detalles: {title}')
        self.setMinimumSize(1000, 600)
        self.questions = questions  # Guardar preguntas para práctica personalizada
        self.parent_widget = parent  # Guardar referencia al widget padre
        
        # Estilo Matrix
        self.setStyleSheet('''
            QDialog {
                background: #000000;
            }
            QLabel {
                color: #00FF00;
                font-family: Courier New, monospace;
            }
            QTableWidget {
                background: #0a0a0a;
                color: #00FF00;
                font-family: Courier New, monospace;
                font-size: 11px;
                border: 2px solid #00FF00;
                gridline-color: #004400;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #002200;
            }
            QTableWidget::item:selected {
                background: #1a3a1a;
                color: #FFFF00;
            }
            QHeaderView::section {
                background: #0a1a0a;
                color: #00FF00;
                font-weight: bold;
                font-size: 12px;
                padding: 10px;
                border: 1px solid #00FF00;
            }
            QPushButton {
                color: #00FF00;
                background: #0a0a0a;
                border: 2px solid #00FF00;
                border-radius: 3px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00FF00;
                color: #000;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel(f'📊 {title}')
        header.setStyleSheet('''
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            background: #0a1a0a;
            border: 2px solid #00FF00;
            border-radius: 3px;
        ''')
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Contador
        count_label = QLabel(f'Total de preguntas: {len(questions)}')
        count_label.setStyleSheet('font-size: 12px; padding: 5px;')
        count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(count_label)
        
        # Tabla
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(['ID', 'Sección', 'Pregunta', 'Aciertos', 'Correctas/Total', 'Estado'])
        table.setRowCount(len(questions))
        
        for i, q in enumerate(questions):
            # ID
            id_item = QTableWidgetItem(str(q['id']))
            id_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 0, id_item)
            
            # Sección
            section_item = QTableWidgetItem(q['section'])
            table.setItem(i, 1, section_item)
            
            # Pregunta (truncada)
            question_text = q['question'][:80] + '...' if len(q['question']) > 80 else q['question']
            question_item = QTableWidgetItem(question_text)
            table.setItem(i, 2, question_item)
            
            # Métricas
            metrics = q.get('metrics', '')
            if metrics:
                try:
                    parts = metrics.split(';')
                    correct = int(parts[0])
                    incorrect = int(parts[1]) if len(parts) > 1 else 0
                    attempts = correct + incorrect
                    accuracy = (correct / attempts * 100) if attempts > 0 else 0
                except:
                    correct = 0
                    incorrect = 0
                    attempts = 0
                    accuracy = 0
            else:
                correct = 0
                incorrect = 0
                attempts = 0
                accuracy = 0
            
            # Dominio (mostrar porcentaje)
            mastery_item = QTableWidgetItem(f'{accuracy:.0f}%')
            mastery_item.setTextAlignment(Qt.AlignCenter)
            if accuracy >= 80:
                mastery_item.setForeground(QColor('#00FF00'))
            elif accuracy >= 40:
                mastery_item.setForeground(QColor('#FFFF00'))
            else:
                mastery_item.setForeground(QColor('#FF8800'))
            table.setItem(i, 3, mastery_item)
            
            # Intentos (mostrar correctas/total)
            attempts_item = QTableWidgetItem(f'{correct}/{attempts}')
            attempts_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 4, attempts_item)
            
            # Estado
            if accuracy >= 80:
                status = '✓ Dominada'
                color = '#00FF00'
            elif accuracy >= 40:
                status = '⚡ Practicar'
                color = '#FFFF00'
            else:
                status = '⭐ Nueva'
                color = '#FF8800'
            
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)
            status_item.setForeground(QColor(color))
            table.setItem(i, 5, status_item)
        
        # Ajustar columnas
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(table)
        
        # Layout de botones
        buttons_layout = QHBoxLayout()
        
        # Botón practicar estas preguntas
        practice_btn = QPushButton('🎯 PRACTICAR ESTAS PREGUNTAS')
        practice_btn.setStyleSheet('''
            QPushButton {
                color: #FFFF00;
                background: #1a1a00;
                border: 2px solid #FFFF00;
                border-radius: 3px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #FFFF00;
                color: #000;
            }
        ''')
        practice_btn.clicked.connect(self.start_custom_practice)
        buttons_layout.addWidget(practice_btn)
        
        # Botón cerrar
        close_btn = QPushButton('CERRAR')
        close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def start_custom_practice(self):
        """Inicia práctica personalizada con las preguntas mostradas"""
        if self.parent_widget and hasattr(self.parent_widget, 'start_custom_practice'):
            self.close()
            self.parent_widget.start_custom_practice(self.questions)
        else:
            QMessageBox.warning(self, 'Error', 'No se pudo iniciar la práctica personalizada.')

class EstudioModulos(QWidget):
    def __init__(self):
        super().__init__()
        
        # ==== CONFIG VENTANA ====
        self.setWindowTitle('Estudio de Módulos DP-700 - Matrix Edition')
        # Ventana maximizada para aprovechar toda la pantalla
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#050505'))
        palette.setColor(QPalette.WindowText, QColor('#00FF00'))
        self.setPalette(palette)
        
        font = QFont('Courier New', 11)
        self.setFont(font)
        
        # ==== ESTADO ====
        # Inicializar gestor de estadísticas
        self.stats_manager = StatsManager()
        self.session_id = None
        self.session_start = None
        
        self.csv_files = [f for f in os.listdir('.') if f.startswith('dp700_') and f.endswith('.csv')]
        self.questions = []
        self.filtered_questions = []
        self.current_question_index = 0
        self.current_question = None
        self.sections = []
        self.correct_answers = 0
        self.total_answered = 0
        self.current_csv_file = None  # Para rastrear el archivo CSV actual
        
        # ==== LAYOUT PRINCIPAL ====
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # ── Header ──
        header = QLabel('SISTEMA DE ESTUDIO DE MÓDULOS DP-700')
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet('''
            color: #00FF00;
            font-size: 18px;
            font-weight: bold;
            background: #0a0a0a;
            border: 2px solid #00FF00;
            border-radius: 3px;
            padding: 10px;
        ''')
        main_layout.addWidget(header)
        
        # ── Selección de módulo y sección ──
        selection_frame = QFrame()
        selection_frame.setStyleSheet('''
            background: #0a0a0a;
            border: 1px solid #00FF00;
            border-radius: 3px;
            padding: 10px;
        ''')
        selection_layout = QVBoxLayout()
        
        # Módulo
        module_layout = QHBoxLayout()
        module_label = QLabel('MÓDULO:')
        module_label.setStyleSheet('color: #00FF00; font-size: 12px; font-weight: bold;')
        module_layout.addWidget(module_label)
        
        self.module_combo = QComboBox()
        self.module_combo.setStyleSheet('''
            QComboBox {
                color: #00FF00;
                background: #101010;
                border: 1px solid #00FF00;
                padding: 5px;
                font-size: 11px;
            }
            QComboBox:hover {
                border: 1px solid #FFFF00;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                color: #00FF00;
                background: #101010;
                selection-background-color: #00FF00;
                selection-color: #000;
            }
        ''')
        self.module_combo.addItems(self.get_module_names())
        self.module_combo.currentIndexChanged.connect(self.load_module)
        module_layout.addWidget(self.module_combo)
        selection_layout.addLayout(module_layout)
        
        # Sección
        section_layout = QHBoxLayout()
        section_label = QLabel('SECCIÓN:')
        section_label.setStyleSheet('color: #00FF00; font-size: 12px; font-weight: bold;')
        section_layout.addWidget(section_label)
        
        self.section_combo = QComboBox()
        self.section_combo.setStyleSheet('''
            QComboBox {
                color: #FFFF00;
                background: #101010;
                border: 1px solid #FFFF00;
                padding: 5px;
                font-size: 11px;
            }
            QComboBox:hover {
                border: 1px solid #00FF00;
            }
            QComboBox QAbstractItemView {
                color: #FFFF00;
                background: #101010;
                selection-background-color: #FFFF00;
                selection-color: #000;
            }
        ''')
        self.section_combo.currentIndexChanged.connect(self.filter_by_section)
        section_layout.addWidget(self.section_combo)
        selection_layout.addLayout(section_layout)
        
        # Panel de Dominio del Módulo
        self.domain_frame = QFrame()
        self.domain_frame.setStyleSheet('''
            QFrame {
                background: #0a0a0a;
                border: 2px solid #00FFFF;
                border-radius: 5px;
                padding: 10px;
            }
        ''')
        domain_layout = QVBoxLayout()
        
        domain_title = QLabel('📊 ESTADÍSTICAS DE DOMINIO')
        domain_title.setAlignment(Qt.AlignCenter)
        domain_title.setStyleSheet('''
            color: #00FFFF;
            font-size: 13px;
            font-weight: bold;
            padding: 5px;
        ''')
        domain_layout.addWidget(domain_title)
        
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(10)
        
        # Total de preguntas
        self.total_questions_label = ClickableLabel('', self.show_all_questions_detail)
        self.total_questions_label.setAlignment(Qt.AlignCenter)
        self.total_questions_label.setStyleSheet('''
            color: #00FF00;
            font-size: 11px;
            background: #001a00;
            padding: 8px;
            border-radius: 3px;
        ''')
        stats_grid.addWidget(self.total_questions_label)
        
        # Dominadas
        self.mastered_label = ClickableLabel('', self.show_mastered_questions_detail)
        self.mastered_label.setAlignment(Qt.AlignCenter)
        self.mastered_label.setStyleSheet('''
            color: #00FF00;
            font-size: 11px;
            background: #001a00;
            padding: 8px;
            border-radius: 3px;
        ''')
        stats_grid.addWidget(self.mastered_label)
        
        # Practicar
        self.practice_label = ClickableLabel('', self.show_practice_questions_detail)
        self.practice_label.setAlignment(Qt.AlignCenter)
        self.practice_label.setStyleSheet('''
            color: #FFFF00;
            font-size: 11px;
            background: #1a1a00;
            padding: 8px;
            border-radius: 3px;
        ''')
        stats_grid.addWidget(self.practice_label)
        
        # Nuevas
        self.new_label = ClickableLabel('', self.show_new_questions_detail)
        self.new_label.setAlignment(Qt.AlignCenter)
        self.new_label.setStyleSheet('''
            color: #FF8800;
            font-size: 11px;
            background: #1a0a00;
            padding: 8px;
            border-radius: 3px;
        ''')
        stats_grid.addWidget(self.new_label)
        
        domain_layout.addLayout(stats_grid)
        
        # Barra de dominio general
        self.domain_bar = QProgressBar()
        self.domain_bar.setFixedHeight(20)
        self.domain_bar.setStyleSheet('''
            QProgressBar {
                border: 2px solid #00FFFF;
                background: #0a0a0a;
                text-align: center;
                font-size: 11px;
                color: #00FFFF;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF0000, stop:0.5 #FFFF00, stop:1 #00FF00);
            }
        ''')
        self.domain_bar.setFormat('%p% Dominio')
        domain_layout.addWidget(self.domain_bar)
        
        self.domain_frame.setLayout(domain_layout)
        selection_layout.addWidget(self.domain_frame)
        self.domain_frame.hide()  # Ocultar hasta que se cargue un módulo
        
        # Botón iniciar
        self.start_btn = QPushButton('INICIAR ESTUDIO ►')
        self.start_btn.setFixedHeight(50)
        self.start_btn.setStyleSheet('''
            QPushButton {
                color: #00FF00;
                background: #101010;
                border: 2px solid #00FF00;
                border-radius: 3px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00FF00;
                color: #000;
            }
        ''')
        self.start_btn.clicked.connect(self.start_study)
        selection_layout.addWidget(self.start_btn)
        
        selection_frame.setLayout(selection_layout)
        main_layout.addWidget(selection_frame)
        
        # ── Progreso ──
        progress_frame = QFrame()
        progress_frame.setStyleSheet('''
            background: #0a0a0a;
            border: 1px solid #00FF00;
            border-radius: 3px;
            padding: 8px;
        ''')
        progress_layout = QVBoxLayout()
        
        self.progress_label = QLabel()
        self.progress_label.setStyleSheet('color: #00FF00; font-size: 11px; font-weight: bold;')
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet('''
            QProgressBar {
                border: 1px solid #004000;
                background: #101010;
            }
            QProgressBar::chunk {
                background: #00FF00;
            }
        ''')
        progress_layout.addWidget(self.progress_bar)
        
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet('color: #00DD00; font-size: 10px;')
        progress_layout.addWidget(self.stats_label)
        
        progress_frame.setLayout(progress_layout)
        main_layout.addWidget(progress_frame)
        self.progress_widget = progress_frame
        progress_frame.hide()
        
        # ── Área de pregunta (con scroll) ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('''
            QScrollArea {
                border: 1px solid #00FF00;
                background: #000;
            }
            QScrollBar:vertical {
                background: #101010;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #00FF00;
                border-radius: 6px;
            }
        ''')
        
        self.question_widget = QWidget()
        self.question_widget.setStyleSheet('''
            QWidget {
                background: #000000;
            }
        ''')
        self.question_layout = QVBoxLayout()
        self.question_layout.setSpacing(12)
        self.question_layout.setContentsMargins(15, 15, 15, 15)
        self.question_widget.setLayout(self.question_layout)
        scroll.setWidget(self.question_widget)
        main_layout.addWidget(scroll)
        self.question_widget.hide()
        
        # ── Botones de control ──
        control_layout = QHBoxLayout()
        
        self.verify_btn = QPushButton('► VERIFICAR RESPUESTA')
        self.verify_btn.setFixedHeight(60)
        self.verify_btn.setStyleSheet('''
            QPushButton {
                color: #FFFF00;
                background: #1a1a00;
                border: 3px solid #FFFF00;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #FFFF00;
                color: #000000;
                border: 3px solid #FFDD00;
            }
            QPushButton:disabled {
                color: #555;
                border-color: #333;
                background: #0a0a0a;
            }
        ''')
        self.verify_btn.clicked.connect(self.verify_answer)
        self.verify_btn.hide()
        control_layout.addWidget(self.verify_btn)
        
        self.next_btn = QPushButton('SIGUIENTE PREGUNTA ►')
        self.next_btn.setFixedHeight(60)
        self.next_btn.setStyleSheet('''
            QPushButton {
                color: #00FF00;
                background: #0a1a0a;
                border: 3px solid #00FF00;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00FF00;
                color: #000000;
                border: 3px solid #00DD00;
            }
        ''')
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.hide()
        control_layout.addWidget(self.next_btn)
        
        main_layout.addLayout(control_layout)
        
        self.setLayout(main_layout)
        
        # Cargar primer módulo
        if self.csv_files:
            self.load_module()
    
    def get_module_names(self):
        """Extrae nombres amigables de los archivos CSV"""
        names = []
        for f in self.csv_files:
            # Quitar dp700_ y .csv, reemplazar _ con espacios
            name = f.replace('dp700_', '').replace('.csv', '').replace('_', ' ').title()
            names.append(name)
        return names if names else ['No hay módulos disponibles']
    
    def show_all_questions_detail(self):
        """Muestra todas las preguntas del módulo"""
        if not self.questions:
            return
        dialog = QuestionDetailsDialog('Todas las Preguntas', self.questions, self)
        dialog.exec_()
    
    def show_mastered_questions_detail(self):
        """Muestra solo las preguntas dominadas (>= 80% aciertos)"""
        if not self.questions:
            return
        mastered_questions = []
        for q in self.questions:
            metrics = q.get('metrics', '')
            if metrics:
                try:
                    parts = metrics.split(';')
                    correct = int(parts[0])
                    incorrect = int(parts[1]) if len(parts) > 1 else 0
                    total = correct + incorrect
                    if total > 0:
                        accuracy = correct / total
                        if accuracy >= 0.8:  # >= 80%
                            mastered_questions.append(q)
                except:
                    pass
        dialog = QuestionDetailsDialog('Preguntas Dominadas (≥80%)', mastered_questions, self)
        dialog.exec_()
    
    def show_practice_questions_detail(self):
        """Muestra preguntas que necesitan práctica (40-79% aciertos)"""
        if not self.questions:
            return
        practice_questions = []
        for q in self.questions:
            metrics = q.get('metrics', '')
            if metrics:
                try:
                    parts = metrics.split(';')
                    correct = int(parts[0])
                    incorrect = int(parts[1]) if len(parts) > 1 else 0
                    total = correct + incorrect
                    if total > 0:
                        accuracy = correct / total
                        if 0.4 <= accuracy < 0.8:  # 40-79%
                            practice_questions.append(q)
                except:
                    pass
        dialog = QuestionDetailsDialog('Preguntas para Practicar (40-79%)', practice_questions, self)
        dialog.exec_()
    
    def show_new_questions_detail(self):
        """Muestra preguntas nuevas (sin métricas o < 40% aciertos)"""
        if not self.questions:
            return
        new_questions = []
        for q in self.questions:
            metrics = q.get('metrics', '')
            if not metrics:
                new_questions.append(q)
            else:
                try:
                    parts = metrics.split(';')
                    correct = int(parts[0])
                    incorrect = int(parts[1]) if len(parts) > 1 else 0
                    total = correct + incorrect
                    if total > 0:
                        accuracy = correct / total
                        if accuracy < 0.4:  # < 40%
                            new_questions.append(q)
                    else:
                        new_questions.append(q)
                except:
                    new_questions.append(q)
        dialog = QuestionDetailsDialog('Preguntas Nuevas (<40%)', new_questions, self)
        dialog.exec_()
    
    def calculate_module_stats(self):
        """Calcula estadísticas de dominio del módulo actual"""
        if not self.questions:
            return
        
        total = len(self.questions)
        mastered = 0   # >= 80% aciertos
        practice = 0   # 40-79% aciertos
        new = 0        # < 40% o sin métricas
        
        total_correct = 0
        total_attempts = 0
        
        for q in self.questions:
            metrics = q.get('metrics', '')
            if metrics:
                try:
                    parts = metrics.split(';')
                    correct = int(parts[0])
                    incorrect = int(parts[1]) if len(parts) > 1 else 0
                    attempts = correct + incorrect
                    
                    total_correct += correct
                    total_attempts += attempts
                    
                    if attempts > 0:
                        accuracy = correct / attempts
                        if accuracy >= 0.8:
                            mastered += 1
                        elif accuracy >= 0.4:
                            practice += 1
                        else:
                            new += 1
                    else:
                        new += 1
                except:
                    new += 1
            else:
                new += 1
        
        # Calcular porcentaje de dominio general
        domain_percentage = int((total_correct / total_attempts * 100)) if total_attempts > 0 else 0
        
        # Actualizar UI
        self.total_questions_label.setText(f'Total\n{total}')
        self.mastered_label.setText(f'✓ Dominadas\n{mastered}')
        self.practice_label.setText(f'⚡ Practicar\n{practice}')
        self.new_label.setText(f'★ Nuevas\n{new}')
        self.domain_bar.setValue(domain_percentage)
        
        self.domain_frame.show()
    
    def load_module(self):
        """Carga las preguntas del módulo seleccionado"""
        if not self.csv_files:
            return
        
        idx = self.module_combo.currentIndex()
        if idx < 0 or idx >= len(self.csv_files):
            return
        
        file_path = self.csv_files[idx]
        self.current_csv_file = file_path  # Guardar referencia
        self.questions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.questions.append(row)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'No se pudo cargar el módulo:\n{e}')
            return
        
        # Extraer secciones únicas
        self.sections = sorted(set(q['section'] for q in self.questions))
        
        # Actualizar combo de secciones
        self.section_combo.clear()
        self.section_combo.addItem('[TODAS LAS SECCIONES]')
        self.section_combo.addItems(self.sections)
        
        # Calcular y mostrar estadísticas de dominio
        self.calculate_module_stats()
    
    def filter_by_section(self):
        """Filtra preguntas por sección"""
        # Se aplicará al iniciar estudio
        pass
    
    def start_study(self):
        """Inicia la sesión de estudio"""
        if not self.questions:
            QMessageBox.warning(self, 'Advertencia', 'No hay preguntas cargadas.')
            return
        
        # Filtrar por sección
        section_idx = self.section_combo.currentIndex()
        if section_idx == 0:  # Todas las secciones
            self.filtered_questions = self.questions.copy()
        else:
            selected_section = self.sections[section_idx - 1]
            self.filtered_questions = [q for q in self.questions if q['section'] == selected_section]
        
        if not self.filtered_questions:
            QMessageBox.warning(self, 'Advertencia', 'No hay preguntas en esta sección.')
            return
        
        # Mezclar preguntas
        random.shuffle(self.filtered_questions)
        
        # Iniciar sesión de tracking
        self.session_id = self.stats_manager.start_session('module_study')
        self.session_start = datetime.now()
        
        # Reiniciar estadísticas
        self.current_question_index = 0
        self.correct_answers = 0
        self.total_answered = 0
        
        # Mostrar controles de estudio
        self.progress_widget.show()
        self.question_widget.show()
        self.verify_btn.show()
        
        # Mostrar primera pregunta
        self.show_question()
    
    def start_custom_practice(self, custom_questions):
        """Inicia práctica personalizada con preguntas específicas"""
        if not custom_questions:
            QMessageBox.warning(self, 'Advertencia', 'No hay preguntas para practicar.')
            return
        
        # Usar las preguntas personalizadas directamente
        self.filtered_questions = custom_questions.copy()
        
        # Mezclar preguntas
        random.shuffle(self.filtered_questions)
        
        # Reiniciar estadísticas
        self.current_question_index = 0
        self.correct_answers = 0
        self.total_answered = 0
        
        # Mostrar controles de estudio
        self.progress_widget.show()
        self.question_widget.show()
        self.verify_btn.show()
        
        # Mostrar primera pregunta
        self.show_question()
    
    def show_question(self):
        """Muestra la pregunta actual"""
        if self.current_question_index >= len(self.filtered_questions):
            self.finish_study()
            return
        
        self.current_question = self.filtered_questions[self.current_question_index]
        
        # Actualizar progreso
        progress = int((self.current_question_index / len(self.filtered_questions)) * 100)
        self.progress_bar.setValue(progress)
        self.progress_label.setText(
            f'[PROGRESO] Pregunta {self.current_question_index + 1} de {len(self.filtered_questions)}'
        )
        self.stats_label.setText(
            f'Correctas: {self.correct_answers}/{self.total_answered} ' +
            f'({int(self.correct_answers/self.total_answered*100) if self.total_answered > 0 else 0}%)'
        )
        
        # Limpiar layout anterior
        for i in reversed(range(self.question_layout.count())): 
            widget = self.question_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Sección
        section_label = QLabel(f'SECCIÓN: {self.current_question["section"]}')
        section_label.setStyleSheet('''
            color: #00FFFF;
            font-size: 11px;
            font-weight: bold;
            padding: 8px;
            background: #001a1a;
            border-left: 4px solid #00FFFF;
            border-radius: 2px;
        ''')
        section_label.setWordWrap(True)
        self.question_layout.addWidget(section_label)
        
        # Métricas de la pregunta
        metrics = self.current_question.get('metrics', '')
        if metrics:
            try:
                parts = metrics.split(';')
                correct = int(parts[0])
                incorrect = int(parts[1]) if len(parts) > 1 else 0
                attempts = correct + incorrect
                
                # Calcular porcentaje de aciertos
                accuracy = (correct / attempts * 100) if attempts > 0 else 0
                
                # Determinar color y etiqueta según porcentaje
                if accuracy >= 80:
                    status = '✓ DOMINADA'
                    color = '#00FF00'
                    bg = '#0a1a0a'
                elif accuracy >= 40:
                    status = '⚡ PRACTICAR'
                    color = '#FFFF00'
                    bg = '#1a1a00'
                else:
                    status = '★ NUEVA'
                    color = '#FF8800'
                    bg = '#1a0a00'
                
                metrics_label = QLabel(
                    f'{status} | Aciertos: {accuracy:.0f}% ({correct}/{attempts}) | Total: {attempts}'
                )
                metrics_label.setStyleSheet(f'''
                    color: {color};
                    font-size: 10px;
                    font-weight: bold;
                    padding: 6px;
                    background: {bg};
                    border: 1px solid {color};
                    border-radius: 3px;
                ''')
                metrics_label.setAlignment(Qt.AlignCenter)
                self.question_layout.addWidget(metrics_label)
            except:
                pass
        else:
            # Sin métricas previas
            new_label = QLabel('★ PREGUNTA NUEVA - Aún no has respondido')
            new_label.setStyleSheet('''
                color: #FF8800;
                font-size: 10px;
                font-weight: bold;
                padding: 6px;
                background: #1a0a00;
                border: 1px solid #FF8800;
                border-radius: 3px;
            ''')
            new_label.setAlignment(Qt.AlignCenter)
            self.question_layout.addWidget(new_label)
        
        # Pregunta
        question_label = QLabel(f'PREGUNTA {self.current_question["id"]}: {self.current_question["question"]}')
        question_label.setStyleSheet('''
            color: #00FF00;
            font-size: 14px;
            font-weight: bold;
            padding: 15px;
            background: #0a1a0a;
            border: 2px solid #00FF00;
            border-radius: 5px;
        ''')
        question_label.setWordWrap(True)
        self.question_layout.addWidget(question_label)
        
        # Opciones (dentro de un frame para mejor visualización)
        options_frame = QFrame()
        options_frame.setStyleSheet('''
            QFrame {
                background: #0a0a0a;
                border: 2px solid #666;
                border-radius: 5px;
                padding: 15px;
            }
        ''')
        options_layout = QVBoxLayout()
        options_layout.setSpacing(10)
        
        options = self.current_question['options'].split(';')
        
        # Crear lista de opciones con sus índices originales (1-based)
        indexed_options = [(i+1, option) for i, option in enumerate(options)]
        
        # Aleatorizar el orden de las opciones
        random.shuffle(indexed_options)
        
        # Guardar el mapeo para verificación posterior
        self.shuffled_mapping = {display_pos: original_idx for display_pos, (original_idx, _) in enumerate(indexed_options, 1)}
        
        self.option_group = QButtonGroup()
        
        for display_pos, (original_idx, option) in enumerate(indexed_options, 1):
            radio = QRadioButton(f'{display_pos}) {option}')
            radio.setStyleSheet('''
                QRadioButton {
                    color: #FFFF00;
                    font-size: 13px;
                    padding: 12px;
                    spacing: 12px;
                    background: transparent;
                }
                QRadioButton:hover {
                    background: #1a1a00;
                    border-radius: 3px;
                }
                QRadioButton::indicator {
                    width: 20px;
                    height: 20px;
                    border: 2px solid #FFFF00;
                    border-radius: 10px;
                    background: #000000;
                }
                QRadioButton::indicator:checked {
                    background: radial-gradient(circle, #FFFF00 40%, #000000 41%);
                    border: 2px solid #FFFF00;
                }
                QRadioButton::indicator:hover {
                    border: 2px solid #00FF00;
                    background: #0a0a0a;
                }
            ''')
            # Usar display_pos como ID del botón
            self.option_group.addButton(radio, display_pos)
            options_layout.addWidget(radio)
        
        options_frame.setLayout(options_layout)
        self.question_layout.addWidget(options_frame)
        
        self.question_layout.addStretch()
        
        # Reiniciar botones
        self.verify_btn.setEnabled(True)
        self.next_btn.hide()
    
    def verify_answer(self):
        """Verifica la respuesta del usuario y actualiza métricas"""
        selected_display_pos = self.option_group.checkedId()
        if selected_display_pos == -1:
            QMessageBox.warning(self, 'Advertencia', 'Selecciona una opción primero.')
            return
        
        # Obtener el índice original de la opción seleccionada
        selected_original_idx = self.shuffled_mapping[selected_display_pos]
        
        # Obtener la respuesta correcta (índice original)
        correct_answer = int(self.current_question['correct'])
        is_correct = (selected_original_idx == correct_answer)
        
        # Encontrar la posición de visualización de la respuesta correcta para el feedback
        correct_display_pos = None
        for display_pos, original_idx in self.shuffled_mapping.items():
            if original_idx == correct_answer:
                correct_display_pos = display_pos
                break
        
        self.total_answered += 1
        if is_correct:
            self.correct_answers += 1
        
        # Registrar respuesta en estadísticas globales
        module_name = self.module_combo.currentText()
        question_id = self.current_question.get('id', 'unknown')
        self.stats_manager.record_module_answer(module_name, question_id, is_correct)
        
        # Actualizar métricas en el CSV
        self.update_metrics(is_correct)
        
        # Actualizar estadísticas
        self.stats_label.setText(
            f'Correctas: {self.correct_answers}/{self.total_answered} ' +
            f'({int(self.correct_answers/self.total_answered*100)}%)'
        )
        
        # Mostrar feedback
        feedback_frame = QFrame()
        feedback_frame.setStyleSheet('''
            QFrame {
                background: #000000;
            }
        ''')
        feedback_layout = QVBoxLayout()
        
        if is_correct:
            result_label = QLabel('✓ CORRECTO')
            result_label.setStyleSheet('''
                color: #00FF00;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                background: #0a1a0a;
                border: 3px solid #00FF00;
                border-radius: 5px;
            ''')
        else:
            result_label = QLabel(f'✗ INCORRECTO - La respuesta correcta es la opción {correct_display_pos}')
            result_label.setStyleSheet('''
                color: #FF0000;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                background: #1a0a0a;
                border: 3px solid #FF0000;
                border-radius: 5px;
            ''')
        result_label.setWordWrap(True)
        feedback_layout.addWidget(result_label)
        
        # Notas
        notes_label = QLabel(f'NOTAS: {self.current_question["notas"]}')
        notes_label.setStyleSheet('''
            color: #00FFFF;
            font-size: 12px;
            padding: 12px;
            background: #001a1a;
            border-left: 4px solid #00FFFF;
            border-radius: 3px;
        ''')
        notes_label.setWordWrap(True)
        feedback_layout.addWidget(notes_label)
        
        # Pregunta de verificación (si existe)
        if self.current_question.get('second_question'):
            second_q_label = QLabel(f'VERIFICACIÓN: {self.current_question["second_question"]}')
            second_q_label.setStyleSheet('''
                color: #FFFF00;
                font-size: 12px;
                font-weight: bold;
                padding: 12px;
                background: #1a1a00;
                border-left: 4px solid #FFFF00;
                border-radius: 3px;
            ''')
            second_q_label.setWordWrap(True)
            feedback_layout.addWidget(second_q_label)
            
            if self.current_question.get('second_explanation'):
                expl_label = QLabel(f'→ {self.current_question["second_explanation"]}')
                expl_label.setStyleSheet('''
                    color: #DDDD00;
                    font-size: 11px;
                    padding: 10px 10px 10px 25px;
                    background: #0a0a00;
                    border-radius: 2px;
                ''')
                expl_label.setWordWrap(True)
                feedback_layout.addWidget(expl_label)
        
        feedback_frame.setLayout(feedback_layout)
        self.question_layout.addWidget(feedback_frame)
        
        # Deshabilitar verificación y mostrar siguiente
        self.verify_btn.setEnabled(False)
        self.next_btn.show()
        
        # Deshabilitar opciones
        for button in self.option_group.buttons():
            button.setEnabled(False)
    
    def next_question(self):
        """Avanza a la siguiente pregunta"""
        self.current_question_index += 1
        self.show_question()
    
    def update_metrics(self, is_correct):
        """Actualiza las métricas de la pregunta en el CSV"""
        if not self.current_csv_file or not self.current_question:
            return
        
        try:
            # Leer el CSV actual
            rows = []
            with open(self.current_csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    rows.append(row)
            
            # Encontrar y actualizar la pregunta actual
            question_id = self.current_question['id']
            section = self.current_question['section']
            
            for row in rows:
                if row['id'] == question_id and row['section'] == section:
                    # Obtener métricas actuales
                    metrics = row.get('metrics', '')
                    if metrics:
                        try:
                            parts = metrics.split(';')
                            correct = int(parts[0])
                            incorrect = int(parts[1]) if len(parts) > 1 else 0
                        except:
                            correct = 0
                            incorrect = 0
                    else:
                        correct = 0
                        incorrect = 0
                    
                    # Actualizar métricas
                    if is_correct:
                        correct += 1
                    else:
                        incorrect += 1
                    
                    # Guardar nuevas métricas
                    row['metrics'] = f'{correct};{incorrect}'
                    
                    # Actualizar también en el objeto actual
                    self.current_question['metrics'] = row['metrics']
                    break
            
            # Escribir de vuelta al CSV
            with open(self.current_csv_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            
            # Actualizar la pregunta en la lista actual sin recargar todo
            for q in self.questions:
                if q['id'] == question_id and q['section'] == section:
                    q['metrics'] = self.current_question['metrics']
                    break
            
            # Recalcular estadísticas del módulo
            self.calculate_module_stats()
            
        except Exception as e:
            print(f'Error al actualizar métricas: {e}')
    
    def finish_study(self):
        """Finaliza la sesión de estudio"""
        # Guardar estadísticas de sesión
        if self.session_id:
            session_stats = {
                'questions_answered': self.total_answered,
                'correct_answers': self.correct_answers,
                'accuracy': int(self.correct_answers / self.total_answered * 100) if self.total_answered > 0 else 0
            }
            self.stats_manager.end_session(self.session_id, session_stats)
        
        self.progress_bar.setValue(100)
        
        # Limpiar layout
        for i in reversed(range(self.question_layout.count())): 
            widget = self.question_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Mensaje final
        final_frame = QFrame()
        final_frame.setStyleSheet('''
            background: #0a1a0a;
            border: 2px solid #00FF00;
            border-radius: 5px;
            padding: 30px;
        ''')
        final_layout = QVBoxLayout()
        
        title = QLabel('★ SESIÓN COMPLETADA ★')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('''
            color: #00FF00;
            font-size: 20px;
            font-weight: bold;
        ''')
        final_layout.addWidget(title)
        
        percentage = int(self.correct_answers / self.total_answered * 100) if self.total_answered > 0 else 0
        score = QLabel(f'PUNTUACIÓN FINAL: {self.correct_answers}/{self.total_answered} ({percentage}%)')
        score.setAlignment(Qt.AlignCenter)
        score.setStyleSheet('''
            color: #FFFF00;
            font-size: 16px;
            font-weight: bold;
            padding: 20px;
        ''')
        final_layout.addWidget(score)
        
        # Mensaje motivacional
        if percentage >= 90:
            msg = '¡EXCELENTE! Dominas el material.'
            color = '#00FF00'
        elif percentage >= 70:
            msg = '¡BUEN TRABAJO! Sigue repasando.'
            color = '#FFFF00'
        else:
            msg = 'Necesitas más práctica. ¡Sigue adelante!'
            color = '#FF8800'
        
        motivation = QLabel(msg)
        motivation.setAlignment(Qt.AlignCenter)
        motivation.setStyleSheet(f'''
            color: {color};
            font-size: 14px;
            padding: 10px;
        ''')
        final_layout.addWidget(motivation)
        
        # Información de progreso en el dominio
        domain_info = QLabel(
            '📊 Las métricas han sido actualizadas.\\n'
            'Tu progreso de dominio se refleja en el panel superior.'
        )
        domain_info.setAlignment(Qt.AlignCenter)
        domain_info.setStyleSheet('''
            color: #00DDDD;
            font-size: 11px;
            padding: 10px;
            background: #001a1a;
            border-radius: 3px;
        ''')
        final_layout.addWidget(domain_info)
        
        restart_btn = QPushButton('REINICIAR ESTUDIO')
        restart_btn.setFixedHeight(50)
        restart_btn.setStyleSheet('''
            QPushButton {
                color: #00FF00;
                background: #101010;
                border: 2px solid #00FF00;
                border-radius: 3px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00FF00;
                color: #000;
            }
        ''')
        restart_btn.clicked.connect(self.restart_study)
        final_layout.addWidget(restart_btn)
        
        final_frame.setLayout(final_layout)
        self.question_layout.addWidget(final_frame)
        
        self.verify_btn.hide()
        self.next_btn.hide()
    
    def restart_study(self):
        """Reinicia el sistema de estudio"""
        self.progress_widget.hide()
        self.question_widget.hide()
        self.verify_btn.hide()
        self.next_btn.hide()
        
        # Limpiar layout
        for i in reversed(range(self.question_layout.count())): 
            widget = self.question_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Recalcular estadísticas del módulo
        self.calculate_module_stats()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EstudioModulos()
    window.showMaximized()  # Ventana maximizada ocupando toda la pantalla
    sys.exit(app.exec_())
