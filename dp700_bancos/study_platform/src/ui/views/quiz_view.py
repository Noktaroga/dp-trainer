"""
Vista de Quiz - Modo de estudio de preguntas
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QRadioButton, QButtonGroup,
    QScrollArea, QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import random

from ..themes.colors import ModernColors, Typography, Spacing, BorderRadius
from ...models.question import Question


class QuizView(QWidget):
    """Vista de Quiz interactivo"""
    
    # Señal para volver al dashboard
    back_to_dashboard = pyqtSignal()
    
    def __init__(self, questions, data_loader, persistence, title="Quiz Mode"):
        super().__init__()
        self.questions = questions
        self.data_loader = data_loader
        self.persistence = persistence
        self.title_text = title
        
        self.current_index = 0
        self.score = 0
        self.answered_correctly = 0
        self.answered_incorrectly = 0
        
        # Mezclar preguntas
        self.quiz_questions = self.questions.copy()
        random.shuffle(self.quiz_questions)
        
        self.setup_ui()
        self.show_question()
    
    def setup_ui(self):
        """Configura la interfaz"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(Spacing.LG)
        main_layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        
        # Header con botón de volver
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self.quiz_questions))
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v de %m preguntas")
        main_layout.addWidget(self.progress_bar)
        
        # Scroll area para la pregunta
        scroll= QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(Spacing.LG)
        
        self.content_widget.setLayout(self.content_layout)
        scroll.setWidget(self.content_widget)
        
        main_layout.addWidget(scroll, 1)
        
        # Botones de navegación
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(Spacing.MD)
        
        self.check_btn = QPushButton("Verificar Respuesta")
        self.check_btn.setMinimumHeight(50)
        self.check_btn.clicked.connect(self.check_answer)
        
        self.next_btn = QPushButton("Siguiente →")
        self.next_btn.setMinimumHeight(50)
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setVisible(False)
        
        nav_layout.addStretch()
        nav_layout.addWidget(self.check_btn)
        nav_layout.addWidget(self.next_btn)
        
        main_layout.addLayout(nav_layout)
        
        self.setLayout(main_layout)
    
    def create_header(self) -> QWidget:
        """Crea el header con título y botón de volver"""
        header = QFrame()
        layout = QHBoxLayout()
        layout.setSpacing(Spacing.MD)
        
        # Botón volver
        back_btn = QPushButton("← Volver")
        back_btn.setProperty("buttonType", "secondary")
        back_btn.clicked.connect(self.back_to_dashboard.emit)
        back_btn.setMaximumWidth(150)
        
        # Título
        title = QLabel(self.title_text)
        title.setProperty("labelType", "title")
        
        # Stats
        self.stats_label = QLabel(f"✅ 0 correctas | ❌ 0 incorrectas")
        self.stats_label.setProperty("labelType", "caption")
        
        layout.addWidget(back_btn)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.stats_label)
        
        header.setLayout(layout)
        return header
    
    def show_question(self):
        """Muestra la pregunta actual"""
        # Limpiar layout anterior
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if self.current_index >= len(self.quiz_questions):
            self.show_results()
            return
        
        question = self.quiz_questions[self.current_index]
        
        # Tarjeta de pregunta
        question_card = QFrame()
        question_card.setProperty("frameType", "card")
        card_layout = QVBoxLayout()
        card_layout.setSpacing(Spacing.MD)
        
        # Número de pregunta
        q_num = QLabel(f"Pregunta {self.current_index + 1} de {len(self.quiz_questions)}")
        q_num.setProperty("labelType", "caption")
        card_layout.addWidget(q_num)
        
        # Módulo y sección
        module_label = QLabel(f"📁 {question.module} → {question.section}")
        module_label.setProperty("labelType", "caption")
        module_label.setStyleSheet(f"color: {ModernColors.LIGHT['primary']};")
        card_layout.addWidget(module_label)
        
        # --- NUEVO: Barra de Métricas de la Pregunta ---
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(Spacing.MD)
        
        # Estilo para las etiquetas de métricas
        metric_style = f"""
            background-color: {ModernColors.LIGHT['bg_tertiary']};
            border-radius: {Spacing.SM}px;
            padding: 4px 8px;
            font-size: {Typography.SIZE_SM}px;
        """
        
        # Datos
        total_attempts = question.times_correct + question.times_incorrect
        accuracy = (question.times_correct / total_attempts * 100) if total_attempts > 0 else 0
        
        lbl_seen = QLabel(f"👁️ Vistas: {question.times_seen}")
        lbl_seen.setStyleSheet(metric_style)
        
        lbl_correct = QLabel(f"✅ Aciertos: {question.times_correct}")
        lbl_correct.setStyleSheet(metric_style + f"color: {ModernColors.LIGHT['success']};")
        
        lbl_incorrect = QLabel(f"❌ Fallos: {question.times_incorrect}")
        lbl_incorrect.setStyleSheet(metric_style + f"color: {ModernColors.LIGHT['error']};")
        
        lbl_acc = QLabel(f"📊 Precisión: {accuracy:.1f}%")
        lbl_acc.setStyleSheet(metric_style + f"font-weight: bold;")
        
        metrics_layout.addWidget(lbl_seen)
        metrics_layout.addWidget(lbl_correct)
        metrics_layout.addWidget(lbl_incorrect)
        metrics_layout.addWidget(lbl_acc)
        metrics_layout.addStretch() # Empujar a la izquierda
        
        card_layout.addLayout(metrics_layout)
        # -----------------------------------------------
        
        # Texto de la pregunta + Contador (layout horizontal)
        q_container = QWidget()
        q_layout = QHBoxLayout(q_container)
        q_layout.setContentsMargins(0, 0, 0, 0)
        
        q_text = QLabel(question.question_text)
        q_text.setWordWrap(True)
        q_text.setStyleSheet(f"""
            font-size: {Typography.SIZE_LG}px;
            font-weight: {Typography.WEIGHT_MEDIUM};
            padding: {Spacing.MD}px 0;
            color: {ModernColors.LIGHT['text_primary']};
        """)
        q_layout.addWidget(q_text, 1) # Expandir texto
        
        # Botón Contador para la Pregunta (Estilo Badge)
        q_counter_btn = QPushButton("0")
        q_counter_btn.setFixedSize(30, 30)
        q_counter_btn.setCursor(Qt.PointingHandCursor)
        q_counter_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ModernColors.LIGHT['bg_tertiary']};
                color: {ModernColors.LIGHT['accent_1']};
                border: 1px solid {ModernColors.LIGHT['accent_1']};
                border-radius: 15px; /* Circular */
                font-weight: bold;
                font-size: 13px;
                margin-left: 10px;
            }}
            QPushButton:hover {{
                background-color: {ModernColors.LIGHT['accent_1']};
                color: {ModernColors.LIGHT['text_inverse']};
            }}
        """)
        q_counter_btn.clicked.connect(lambda checked, b=q_counter_btn: self.increment_counter(b))
        q_layout.addWidget(q_counter_btn)
        
        card_layout.addWidget(q_container)
        
        # Opciones (radio buttons)
        self.options_group = QButtonGroup()
        
        # Preparar opciones mezcladas
        # Lista de tuplas: (Texto, EsCorrecta, IndiceOriginal)
        options_data = []
        for i, opt_text in enumerate(question.options):
            is_correct = (i == question.correct_answer)
            options_data.append({'text': opt_text, 'is_correct': is_correct, 'orig_idx': i})
            
        # Mezclar aleatoriamente
        random.shuffle(options_data)
        self.current_shuffled_options = options_data # Guardar para validación
        
        # Lista para seguimiento de botones contadores
        self.option_counters = []

        for i, opt_data in enumerate(options_data):
            # Contenedor horizontal para Opción + Botón Contador
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(Spacing.SM)
            
            # Opción (Radio Button)
            radio = QRadioButton(opt_data['text'])
            radio.setStyleSheet(f"""
                QRadioButton {{
                    padding: {Spacing.MD}px;
                    font-size: {Typography.SIZE_BASE}px;
                }}
            """)
            self.options_group.addButton(radio, i)
            row_layout.addWidget(radio, 1) # Expandir para ocupar espacio
            
            # Botón Contador (Estilo Badge sutil)
            counter_btn = QPushButton("0")
            counter_btn.setFixedSize(28, 28)
            counter_btn.setCursor(Qt.PointingHandCursor)
            
            # Estilo del contador
            counter_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {ModernColors.LIGHT['text_secondary']};
                    border: 1px solid {ModernColors.LIGHT['border']};
                    border-radius: 14px;
                    font-weight: bold;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {ModernColors.LIGHT['primary_light']};
                    color: {ModernColors.LIGHT['primary']};
                    border-color: {ModernColors.LIGHT['primary']};
                }}
            """)
            
            # Conectar clic para incrementar
            counter_btn.clicked.connect(lambda checked, b=counter_btn: self.increment_counter(b))
            
            self.option_counters.append(counter_btn)
            row_layout.addWidget(counter_btn)
            
            card_layout.addWidget(row_widget)
        
        # Feedback (inicialmente oculto)
        self.feedback_frame = QFrame()
        self.feedback_frame.setVisible(False)
        feedback_layout = QVBoxLayout()
        
        self.feedback_label = QLabel()
        self.feedback_label.setWordWrap(True)
        feedback_layout.addWidget(self.feedback_label)
        
        self.explanation_label = QLabel()
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setProperty("labelType", "caption")
        feedback_layout.addWidget(self.explanation_label)
        
        self.feedback_frame.setLayout(feedback_layout)
        card_layout.addWidget(self.feedback_frame)
        
        question_card.setLayout(card_layout)
        self.content_layout.addWidget(question_card)
        self.content_layout.addStretch()
        
        # Actualizar UI
        self.check_btn.setVisible(True)
        self.next_btn.setVisible(False)
        self.progress_bar.setValue(self.current_index)
    
    def check_answer(self):
        """Verifica la respuesta basada en opciones mezcladas"""
        selected_id = self.options_group.checkedId()
        
        if selected_id == -1: return
        
        question = self.quiz_questions[self.current_index]
        
        # Validar contra nuestras opciones mezcladas
        user_choice = self.current_shuffled_options[selected_id]
        is_correct = user_choice['is_correct']
        
        # Actualizar métricas
        if is_correct:
            self.answered_correctly += 1
            question.times_correct += 1
        else:
            self.answered_incorrectly += 1
            question.times_incorrect += 1
        question.times_seen += 1
        
        # GUARDAR EN TIEMPO REAL
        if self.data_loader:
            self.data_loader.update_question_stats(question)
        
        # Buscar texto de respuesta correcta para feedback
        correct_text = next((opt['text'] for opt in self.current_shuffled_options if opt['is_correct']), "Desconocida")


        
        # Mostrar feedback
        if is_correct:
            self.feedback_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {ModernColors.LIGHT['success_light']};
                    border-left: 4px solid {ModernColors.LIGHT['success']};
                    border-radius: {Spacing.SM}px;
                    padding: {Spacing.MD}px;
                }}
            """)
            self.feedback_label.setText("✅ ¡Correcto!")
            self.feedback_label.setStyleSheet(f"color: {ModernColors.LIGHT['success']}; font-weight: {Typography.WEIGHT_BOLD};")
        else:
            self.feedback_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {ModernColors.LIGHT['error_light']};
                    border-left: 4px solid {ModernColors.LIGHT['error']};
                    border-radius: {Spacing.SM}px;
                    padding: {Spacing.MD}px;
                }}
            """)
            self.feedback_label.setText(f"❌ Incorrecto. La respuesta correcta es: {correct_text}")
            self.feedback_label.setStyleSheet(f"color: {ModernColors.LIGHT['error']}; font-weight: {Typography.WEIGHT_BOLD};")
        
        if question.explanation:
            self.explanation_label.setText(f"💡 {question.explanation}")
        
        self.feedback_frame.setVisible(True)
        
        # Deshabilitar opciones
        for button in self.options_group.buttons():
            button.setEnabled(False)
        
        # Actualizar UI
        self.check_btn.setVisible(False)
        self.next_btn.setVisible(True)
        self.stats_label.setText(f"✅ {self.answered_correctly} correctas | ❌ {self.answered_incorrectly} incorrectas")
    
    def next_question(self):
        """Avanza a la siguiente pregunta"""
        self.current_index += 1
        self.show_question()
    
    def show_results(self):
        """Muestra los resultados finales"""
        # Limpiar layout
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Tarjeta de resultados
        results_card = QFrame()
        results_card.setProperty("frameType", "card")
        results_layout = QVBoxLayout()
        results_layout.setSpacing(Spacing.XL)
        results_layout.setAlignment(Qt.AlignCenter)
        
        # Título
        title = QLabel("🎉 ¡Quiz Completado!")
        title.setProperty("labelType", "title")
        title.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(title)
        
        # Estadísticas
        total = self.answered_correctly + self.answered_incorrectly
        accuracy = (self.answered_correctly / total * 100) if total > 0 else 0
        
        accuracy_label = QLabel(f"{accuracy:.0f}%")
        accuracy_label.setStyleSheet(f"""
            font-size: {Typography.SIZE_5XL}px;
            font-weight: {Typography.WEIGHT_BOLD};
            color: {ModernColors.LIGHT['primary']};
        """)
        accuracy_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(accuracy_label)
        
        stats_text = QLabel(f"✅ {self.answered_correctly} correctas | ❌ {self.answered_incorrectly} incorrectas")
        stats_text.setProperty("labelType", "subtitle")
        stats_text.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(stats_text)
        
        # Botón volver
        back_btn = QPushButton("← Volver al Dashboard")
        back_btn.setMinimumHeight(60)
        back_btn.clicked.connect(self.back_to_dashboard.emit)
        results_layout.addWidget(back_btn)
        
        results_card.setLayout(results_layout)
        self.content_layout.addWidget(results_card)
        
        # Ocultar botones de navegación
        self.check_btn.setVisible(False)
        self.next_btn.setVisible(False)
        self.progress_bar.setValue(len(self.quiz_questions))
    def increment_counter(self, btn):
        """Incrementa el contador del botón"""
        try:
            current_val = int(btn.text())
            btn.setText(str(current_val + 1))
        except ValueError:
            pass
