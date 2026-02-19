"""
Dashboard principal - CON ESTADÍSTICAS REALES DEL CSV
"""
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QGridLayout, QStackedWidget
)
from PyQt5.QtCore import Qt

from ..themes.colors import ModernColors, Typography, Spacing
from ...services.data_loader import DataLoader
from ...services.persistence import PersistenceService
from ...utils.pomodoro_timer import PomodoroTimer
from ..components.pomodoro_widget import PomodoroWidget

class StatCard(QFrame):
    """Tarjeta de estadística moderna y legible"""
from .quiz_view import QuizView


class StatCard(QFrame):
    """Tarjeta de estadística moderna y legible"""
    
    def __init__(self, title: str, value: str, subtitle: str = ""):
        super().__init__()
        self.setup_ui(title, value, subtitle)
    
    def setup_ui(self, title, value, subtitle):
        """Configura la UI de la tarjeta"""
        self.setProperty("frameType", "card")
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.SM)
        
        # Título
        title_label = QLabel(title)
        title_label.setProperty("labelType", "caption")
        title_label.setWordWrap(True)
        
        # Valor principal (grande y prominente)
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: {Typography.SIZE_3XL}px;
            font-weight: {Typography.WEIGHT_BOLD};
            color: {ModernColors.LIGHT['primary']};
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setProperty("labelType", "caption")
            subtitle_label.setWordWrap(True)
            layout.addWidget(subtitle_label)
        
        layout.addStretch()
        self.setLayout(layout)
        self.setMinimumHeight(120)


class ModeCard(QFrame):
    """Tarjeta de modo de estudio"""
    
    def __init__(self, icon: str, title: str, description: str, count: str = "", callback=None):
        super().__init__()
        self.callback = callback
        self.setup_ui(icon, title, description, count)
    
    def setup_ui(self, icon, title, description, count):
        """Configura la UI"""
        self.setProperty("frameType", "card")
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.MD)
        
        # Ícono grande
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: {Typography.SIZE_5XL}px;")
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Título con contador si existe
        title_text = f"{title}"
        if count:
            title_text += f" ({count})"
        title_label = QLabel(title_text)
        title_label.setProperty("labelType", "subtitle")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        
        # Descripción
        desc_label = QLabel(description)
        desc_label.setProperty("labelType", "caption")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        
        # Botón
        btn = QPushButton("Comenzar →")
        btn.setMinimumHeight(50)
        if self.callback:
            btn.clicked.connect(self.callback)
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(btn)
        
        self.setLayout(layout)
        self.setMinimumHeight(300)


class DashboardView(QWidget):
    """
    Dashboard con estadísticas REALES del CSV
    """
    
    def __init__(self):
        super().__init__()
        # Inicializarservicios
        self.data_loader = DataLoader()
        self.persistence = PersistenceService()
        self.user_stats = self.persistence.load_user_stats()
        
        # Referencia a ventana padre (será seteada por MainWindow)
        self.parent_window = None
        
        # Cargar datos
        self.load_data()
        
        # Inicializar Pomodoro
        self.pomodoro_timer = PomodoroTimer()
        self.pomodoro_ui = PomodoroWidget(self.pomodoro_timer)
        self.mode_cards = [] # Para guardarlos y deshabilitarlos
        
        self.setup_ui()
        self.update_access(False) # Bloquear acceso inicialmente
    
    def load_data(self):
        """Carga datos de comandos y preguntas CON MÉTRICAS"""
        try:
            self.commands = self.data_loader.load_all_commands()
            self.questions = self.data_loader.load_all_questions()
            self.modules_summary = self.data_loader.get_modules_summary()
            
            # Calcular estadísticas agregadas de las métricas del CSV
            self.questions_stats = self.data_loader.calculate_questions_stats(self.questions)
            
            # Calcular precisión global real del CSV
            total_attempts = self.questions_stats['total_correct'] + self.questions_stats['total_incorrect']
            if total_attempts > 0:
                self.global_accuracy = (self.questions_stats['total_correct'] / total_attempts) * 100
            else:
                self.global_accuracy = 0.0
            
            print(f"✅ Cargados: {len(self.commands)} comandos, {len(self.questions)} preguntas")
            print(f"📊 Estadísticas del CSV:")
            print(f"   - Vistas: {self.questions_stats['seen']}")
            print(f"   - Masterizadas (≥80%): {self.questions_stats['mastered']}")
            print(f"   - En aprendizaje (50-79%): {self.questions_stats['learning']}")
            print(f"   - Nuevas (<50%): {self.questions_stats['new']}")
            print(f"   - Precisión global: {self.global_accuracy:.1f}%")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            import traceback
            traceback.print_exc()
            self.commands = []
            self.questions = []
            self.modules_summary = {}
            self.questions_stats = {
                'total': 0, 'mastered': 0, 'learning': 0, 'new': 0,
                'seen': 0, 'total_correct': 0, 'total_incorrect': 0
            }
            self.global_accuracy = 0.0
    
    def setup_ui(self):
        """Configura la interfaz"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(Spacing.XL)
        main_layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        
        # Header elegante
        header = self.create_header()
        main_layout.addWidget(header)
        
        # --- POMODORO ---
        main_layout.addWidget(self.pomodoro_ui)
        
        # Conectar señales del Pomodoro para bloquear/desbloquear
        self.pomodoro_ui.timer_started.connect(lambda: self.update_access(True))
        self.pomodoro_ui.timer_paused.connect(lambda: self.update_access(False))
        self.pomodoro_ui.timer_stopped.connect(lambda: self.update_access(False))
        # ----------------
        
        # Scroll area para contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(Spacing.XL)
        
        # Estadísticas
        stats_section = self.create_stats_section()
        content_layout.addWidget(stats_section)
        
        # Modos de estudio
        modes_section = self.create_modes_section()
        content_layout.addWidget(modes_section)
        
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    def create_header(self) -> QWidget:
        """Crea el header del dashboard"""
        header = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.SM)
        
        # Título principal
        title = QLabel("DP-700 Study Platform")
        title.setProperty("labelType", "title")
        
        # Subtítulo
        subtitle = QLabel("Microsoft Fabric Data Engineer - Con Progreso Real")
        subtitle.setProperty("labelType", "caption")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        header.setLayout(layout)
        return header
    
    def create_stats_section(self) -> QWidget:
        """Crea la sección de estadísticas CON DATOS REALES DEL CSV"""
        section = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.MD)
        
        # Título de sección
        section_title = QLabel("📊 Tu Progreso Real")
        section_title.setProperty("labelType", "subtitle")
        layout.addWidget(section_title)
        
        # Grid de estadísticas (responsive)
        grid = QGridLayout()
        grid.setSpacing(Spacing.MD)
        
        # VALORES REALES DEL CSV
        total_questions = str(len(self.questions))
        questions_seen = str(self.questions_stats['seen'])
        questions_mastered = str(self.questions_stats['mastered'])
        questions_learning = str(self.questions_stats['learning'])
        questions_new = str(self.questions_stats['new'])
        
        # Precisión REAL del CSV
        accuracy = f"{self.global_accuracy:.0f}%"
        
        # Tarjetas con valores REALES
        stats = [
            ("Total Preguntas", total_questions, "En la biblioteca"),
            ("Preguntas Vistas", questions_seen, f"de {total_questions}"),
            ("✅ Masterizadas", questions_mastered, "≥ 80% precisión"),
            ("📚 En Aprendizaje", questions_learning, "50-79% precisión"),
            ("⭐ Nuevas/Practicar", questions_new, "< 50% precisión"),
            ("Precisión Global", accuracy, "De tus respuestas"),
        ]
        
        for i, (title, value, subtitle) in enumerate(stats):
            card = StatCard(title, value, subtitle)
            row = i // 3
            col = i % 3
            grid.addWidget(card, row, col)
        
        layout.addLayout(grid)
        section.setLayout(layout)
        return section
    
    def create_modes_section(self) -> QWidget:
        """Crea la sección de modos de estudio"""
        section = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.MD)
        
        # Título
        section_title = QLabel("🎯 Modos de Estudio")
        section_title.setProperty("labelType", "subtitle")
        layout.addWidget(section_title)
        
        # Grid de modos
        grid = QGridLayout()
        grid.setSpacing(Spacing.LG)
        
        # Modos con contadores reales
        total_modules = len(self.modules_summary)
        modes = [
            ("💻", "SQL Trainer", "Practica comandos SQL con validación en tiempo real", 
             str(len(self.commands)), self.open_sql_trainer),
            ("📚", "Quiz Mode", f"Responde preguntas de {total_modules} módulos", 
             str(len(self.questions)), self.open_study_selection),
            ("📈", "Estadísticas", "Revisa tu progreso detallado", "", self.open_statistics),
        ]
        
        for i, (icon, title, desc, count, callback) in enumerate(modes):
            card = ModeCard(icon, title, desc, count, callback)
            grid.addWidget(card, 0, i)
            self.mode_cards.append(card)
        
        layout.addLayout(grid)
        section.setLayout(layout)
        return section
    
    def update_access(self, enabled):
        """Habilita o deshabilita los modos de estudio según el Pomodoro"""
        for card in self.mode_cards:
            card.setEnabled(enabled)
            # Aplicar estilo visual de deshabilitado
            if enabled:
                card.setStyleSheet("")
                card.setCursor(Qt.PointingHandCursor)
            else:
                card.setStyleSheet(f"""
                    QFrame[frameType="card"] {{
                        background-color: {ModernColors.LIGHT['bg_tertiary']};
                        opacity: 0.6;
                        color: {ModernColors.LIGHT['text_tertiary']};
                    }}
                """)
                card.setCursor(Qt.ForbiddenCursor)

    def open_study_selection(self):
        """Abre la vista de config de estudio"""
        if self.parent_window:
            self.parent_window.show_study_selection()
            
    def open_sql_trainer(self):
        """Abre la vista de SQL Trainer"""
        if self.parent_window:
            self.parent_window.show_sql_trainer()

    def open_statistics(self):
        """Abre estadísticas"""
        if self.parent_window:
            self.parent_window.show_statistics()
