"""
DP-700 Study Platform
Punto de entrada principal con navegación entre vistas
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

from config import Config
from src.ui.themes.colors import ModernColors, BorderRadius
from src.ui.themes.modern_light import ModernLightTheme
from src.ui.views.dashboard_view import DashboardView
from src.ui.views.study_selection_view import StudySelectionView
from src.ui.views.quiz_view import QuizView
from src.ui.views.sql_trainer_view import SQLTrainerView
from src.ui.views.statistics_view import StatisticsView
from src.ui.components.notepad_view import NotepadView


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación con navegación entre vistas"""
    
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.apply_theme()
        self.setup_ui()
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.setWindowTitle(Config.WINDOW_TITLE)
        self.setMinimumSize(Config.WINDOW_MIN_WIDTH, Config.WINDOW_MIN_HEIGHT)
        
        # Centrar ventana
        screen = QApplication.desktop().screenGeometry()
        x = (screen.width() - Config.WINDOW_MIN_WIDTH) // 2
        y = (screen.height() - Config.WINDOW_MIN_HEIGHT) // 2
        self.move(x, y)
    
    def apply_theme(self):
        """Aplica el tema visual"""
        theme = ModernLightTheme()
        self.setStyleSheet(theme.get_stylesheet())
    
    def setup_ui(self):
        """Configura la interfaz con barra superior y stack de vistas"""
        # Contenedor principal
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Barra Superior (Header) ---
        self.header = QWidget()
        self.header.setFixedHeight(60)
        self.header.setStyleSheet(f"background-color: {ModernColors.LIGHT['bg_primary']}; border-bottom: 1px solid {ModernColors.LIGHT['border']};")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # Logo/Título
        app_title = QLabel(Config.WINDOW_TITLE)
        app_title.setStyleSheet(f"color: {ModernColors.LIGHT['primary']}; font-weight: bold; font-size: 18px;")
        header_layout.addWidget(app_title)
        
        header_layout.addStretch()
        
        # Botón Notas (Siempre visible)
        self.btn_notes = QPushButton("📝 Notas")
        self.btn_notes.setCursor(Qt.PointingHandCursor)
        self.btn_notes.setStyleSheet(f"""
            QPushButton {{
                background-color: {ModernColors.LIGHT['surface']};
                color: {ModernColors.LIGHT['text_primary']};
                border: 1px solid {ModernColors.LIGHT['border']};
                border-radius: {BorderRadius.MD}px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ModernColors.LIGHT['surface_elevated']};
                border-color: {ModernColors.LIGHT['primary']};
                color: {ModernColors.LIGHT['primary']};
            }}
        """)
        self.btn_notes.clicked.connect(self.toggle_notepad)
        header_layout.addWidget(self.btn_notes)
        
        main_layout.addWidget(self.header)
        
        # --- Stack Central ---
        self.stack = QStackedWidget()
        
        # Dashboard como vista principal
        self.dashboard = DashboardView()
        self.dashboard.parent_window = self
        self.stack.addWidget(self.dashboard)
        
        main_layout.addWidget(self.stack)
        
        self.setCentralWidget(main_container)
        
        # Inicializar Notepad oculto
        self.notepad = NotepadView(self)
        self.notepad.hide()

    def toggle_notepad(self):
        """Muestra u oculta el notepad"""
        if self.notepad.isVisible():
            self.notepad.hide()
        else:
            # Posicionar 
            self.notepad.show()
            self.notepad.raise_()
    
    def show_study_selection(self):
        """Muestra la vista de selección de estudio"""
        questions = self.dashboard.questions
        data_loader = self.dashboard.data_loader
        persistence = self.dashboard.persistence
        
        selection_view = StudySelectionView(questions, data_loader, persistence)
        selection_view.back_to_dashboard.connect(self.show_dashboard)
        selection_view.start_quiz_signal.connect(self.show_quiz)
        
        self.stack.addWidget(selection_view)
        self.stack.setCurrentWidget(selection_view)

    def show_sql_trainer(self):
        """Muestra la vista de SQL Trainer"""
        commands = self.dashboard.commands
        data_loader = self.dashboard.data_loader
        persistence = self.dashboard.persistence
        
        trainer_view = SQLTrainerView(commands, data_loader, persistence)
        trainer_view.back_to_dashboard.connect(self.show_dashboard)
        
        self.stack.addWidget(trainer_view)
        self.stack.setCurrentWidget(trainer_view)

    def show_statistics(self):
        """Muestra la vista de Estadísticas"""
        questions = self.dashboard.questions
        user_stats = self.dashboard.user_stats
        persistence = self.dashboard.persistence
        
        commands = self.dashboard.commands
        
        stats_view = StatisticsView(questions, user_stats, persistence, commands=commands)
        stats_view.back_to_dashboard.connect(self.show_dashboard)
        
        self.stack.addWidget(stats_view)
        self.stack.setCurrentWidget(stats_view)

    def show_quiz(self, questions, title="Quiz Mode"):
        """Muestra la vista de Quiz con preguntas filtradas"""
        data_loader = self.dashboard.data_loader
        persistence = self.dashboard.persistence
        
        quiz_view = QuizView(questions, data_loader, persistence, title=title)
        quiz_view.back_to_dashboard.connect(self.show_dashboard)
        self.stack.addWidget(quiz_view)
        self.stack.setCurrentWidget(quiz_view)

    def show_dashboard(self):
        """Vuelve al Dashboard"""
        self.stack.setCurrentWidget(self.dashboard)


if __name__ == "__main__":
    # Configurar escalado para pantallas HDPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    
    # Establecer fuente global por si acaso
    # font = app.font()
    # font.setFamily("Clean")
    # app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
