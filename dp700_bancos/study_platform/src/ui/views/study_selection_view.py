"""
Vista de Selección de Estudio - Submenú para elegir modo de Quiz
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGridLayout, QComboBox, 
    QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from ..themes.colors import ModernColors, Typography, Spacing, BorderRadius

class StudyOptionCard(QFrame):
    """Tarjeta seleccionable para opciones de estudio"""
    def __init__(self, title, description, icon, mode_id, parent_view):
        super().__init__()
        self.mode_id = mode_id
        self.parent_view = parent_view
        self.setup_ui(title, description, icon)

    def setup_ui(self, title, description, icon):
        self.setCursor(Qt.PointingHandCursor)
        self.setProperty("frameType", "card")
        
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.SM)
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: {Typography.SIZE_4XL}px;")
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Título
        title_label = QLabel(title)
        title_label.setProperty("labelType", "subtitle")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Descripción
        desc_label = QLabel(description)
        desc_label.setProperty("labelType", "caption")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.parent_view.select_mode(self.mode_id)
        # Efecto visual de selección
        self.setStyleSheet(f"""
            QFrame[frameType="card"] {{
                border: 2px solid {ModernColors.LIGHT['primary']};
                background-color: {ModernColors.LIGHT['primary_light']};
            }}
        """)
        # Resetear otros
        for card in self.parent_view.option_cards:
            if card != self:
                card.setStyleSheet("")  # Volver al estilo por defecto del tema


class StudySelectionView(QWidget):
    """Vista para configurar la sesión de estudio"""
    
    # Señales: mode, questions_subset
    start_quiz_signal = pyqtSignal(list, str) 
    back_to_dashboard = pyqtSignal()

    def __init__(self, questions, data_loader, persistence):
        super().__init__()
        self.all_questions = questions
        self.data_loader = data_loader
        self.persistence = persistence
        self.course_structure = self.data_loader.get_course_structure(questions)
        
        self.selected_mode = "random" # Default
        self.option_cards = []
        
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(Spacing.XL)
        main_layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # 1. Selección de MODO
        mode_label = QLabel("1. Selecciona tu Modo de Estudio")
        mode_label.setProperty("labelType", "subtitle")
        main_layout.addWidget(mode_label)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(Spacing.LG)

        # Opción 1: Aleatorio Global
        card_random = StudyOptionCard(
            "Aleatorio Global", 
            "Mezcla preguntas de todos los módulos para un repaso general.", 
            "🎲", "random", self
        )
        self.option_cards.append(card_random)
        cards_layout.addWidget(card_random)

        # Opción 2: Por Módulo/Sección
        card_topic = StudyOptionCard(
            "Por Tema", 
            "Enfócate en un Módulo específico o una Sección concreta.", 
            "📁", "topic", self
        )
        self.option_cards.append(card_topic)
        cards_layout.addWidget(card_topic)

        # Opción 3: Áreas Débiles (Smart)
        card_smart = StudyOptionCard(
            "Áreas Débiles", 
            "Preguntas nuevas o que has fallado anteriormente.", 
            "🧠", "weak", self
        )
        self.option_cards.append(card_smart)
        cards_layout.addWidget(card_smart)

        main_layout.addLayout(cards_layout)

        # 2. Configuración Específica (Panel Dinámico)
        self.config_frame = QFrame()
        self.config_frame.setProperty("frameType", "elevated")
        self.config_layout = QVBoxLayout(self.config_frame)
        self.update_config_panel() # Inicia con config de random
        
        main_layout.addWidget(self.config_frame)
        
        # Botón Iniciar
        self.start_btn = QPushButton("Comenzar Sesión de Estudio →")
        self.start_btn.setMinimumHeight(60)
        self.start_btn.setStyleSheet(f"font-size: {Typography.SIZE_XL}px; font-weight: bold;")
        self.start_btn.clicked.connect(self.start_study)
        main_layout.addWidget(self.start_btn)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
        
        # Seleccionar random por defecto visualmente
        card_random.mousePressEvent(None)

    def create_header(self):
        header = QFrame()
        layout = QHBoxLayout()
        
        back_btn = QPushButton("← Volver")
        back_btn.setProperty("buttonType", "secondary")
        back_btn.clicked.connect(self.back_to_dashboard.emit)
        
        title = QLabel("Configurar Estudio")
        title.setProperty("labelType", "title")
        title.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(back_btn)
        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        # Spacer para centrar título
        dummy = QWidget()
        dummy.setFixedWidth(back_btn.sizeHint().width())
        layout.addWidget(dummy)
        
        header.setLayout(layout)
        return header

    def select_mode(self, mode):
        self.selected_mode = mode
        self.update_config_panel()

    def clear_layout(self, layout):
        """Elimina recursivamente todos los elementos de un layout"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout is not None:
                        self.clear_layout(sub_layout)

    def update_config_panel(self):
        # Limpieza profunda del layout actual
        self.clear_layout(self.config_layout)

        if self.selected_mode == "random":
            lbl = QLabel("Se seleccionarán preguntas aleatorias de toda la base de datos.")
            lbl.setWordWrap(True)
            self.config_layout.addWidget(lbl)

        elif self.selected_mode == "topic":
            # Selectores de Módulo y Sección
            grid = QGridLayout()
            grid.setSpacing(Spacing.MD)
            
            # Módulo
            lbl_mod = QLabel("Módulo:")
            lbl_mod.setStyleSheet(f"font-weight: {Typography.WEIGHT_BOLD};")
            grid.addWidget(lbl_mod, 0, 0)
            
            self.combo_module = QComboBox()
            self.combo_module.setMinimumWidth(300)
            self.combo_module.addItem("Todos los Módulos", "all")
            for module in self.course_structure.keys():
                self.combo_module.addItem(module, module)
            self.combo_module.currentIndexChanged.connect(self.update_sections)
            grid.addWidget(self.combo_module, 0, 1)
            
            # Sección
            lbl_sec = QLabel("Sección:")
            lbl_sec.setStyleSheet(f"font-weight: {Typography.WEIGHT_BOLD};")
            grid.addWidget(lbl_sec, 1, 0)
            
            self.combo_section = QComboBox()
            self.combo_section.setMinimumWidth(300)
            self.combo_section.addItem("Todas las Secciones", "all")
            self.combo_section.setEnabled(False) # Deshabilitado si es All Modules
            grid.addWidget(self.combo_section, 1, 1)
            
            self.config_layout.addLayout(grid)
            
        elif self.selected_mode == "weak":
            lbl = QLabel("Prioridad: Preguntas nunca vistas + Preguntas con < 50% de precisión.")
            lbl.setWordWrap(True)
            self.config_layout.addWidget(lbl)

    def update_sections(self):
        module_data = self.combo_module.currentData()
        self.combo_section.clear()
        self.combo_section.addItem("Todas las Secciones", "all")
        
        if module_data == "all":
            self.combo_section.setEnabled(False)
        else:
            self.combo_section.setEnabled(True)
            sections = self.course_structure.get(module_data, [])
            for section in sections:
                self.combo_section.addItem(section, section)

    def start_study(self):
        filtered_questions = []
        
        if self.selected_mode == "random":
            filtered_questions = self.all_questions.copy()
            
        elif self.selected_mode == "topic":
            mod = self.combo_module.currentData()
            sec = self.combo_section.currentData()
            
            for q in self.all_questions:
                match_mod = (mod == "all" or q.module == mod)
                match_sec = (sec == "all" or q.section == sec)
                
                if match_mod and match_sec:
                    filtered_questions.append(q)
                    
        elif self.selected_mode == "weak":
            # Estrategia Escalona:
            # 1. Prioridad Máxima: Nuevas o Críticas (< 50%)
            critical = [q for q in self.all_questions if q.times_seen == 0 or q.accuracy < 50]
            
            # 2. Prioridad Media: En aprendizaje (50-79%)
            learning = [q for q in self.all_questions if 50 <= q.accuracy < 80 and q.times_seen > 0]
            
            # Combinar: Primero críticas, luego aprendizaje
            filtered_questions = critical + learning
            
            # Si aún así no hay NINGUNA pregunta débil (todo masterizado al 100%)
            if not filtered_questions:
                # Fallback suave: Tomar algunas aleatorias de las masterizadas para repaso
                import random
                passed = [q for q in self.all_questions if q.accuracy >= 80]
                filtered_questions = random.sample(passed, min(len(passed), 10))
                # O si no hay nada de nada (banco vacío), fallback total
                if not filtered_questions:
                    filtered_questions = self.all_questions.copy()

        if not filtered_questions:
            # Fallback final de seguridad
            filtered_questions = self.all_questions.copy()

        if not filtered_questions:
            # Mostrar alerta o manejar error (aquí simplificado)
            print("No matching questions found!")
            return

        # Emitir señal para cambiar a QuizView con las preguntas filtradas
        # El string es el título del modo para mostrar en el quiz
        mode_title = {
            "random": "🎲 Modo Aleatorio",
            "topic": f"📁 {self.combo_module.currentText() if self.selected_mode == 'topic' else ''}",
            "weak": "🧠 Áreas Débiles"
        }.get(self.selected_mode, "Quiz")
        
        self.start_quiz_signal.emit(filtered_questions, mode_title)
