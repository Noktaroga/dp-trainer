"""
Menu Principal v2.0 - Dashboard Mejorado
Sistema de lanzamiento con estadísticas, logros y accesos rápidos
"""

import sys
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGridLayout, QScrollArea, QProgressBar
)
from PyQt5.QtGui import QColor, QPalette, QFont, QCursor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from stats_manager import StatsManager


class StatCard(QFrame):
    """Tarjeta de estadística animada"""
    
    def __init__(self, title, value, icon, color='#00FF00', parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.setStyleSheet(f'''
            QFrame {{
                background: #0a0a0a;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
            }}
            QFrame:hover {{
                background: #0f0f0f;
                border: 3px solid {color};
            }}
        ''')
        
        layout = QVBoxLayout()
        
        # Ícono + Título
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f'color: {color}; font-size: 28px;')
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f'''
            color: {color};
            font-size: 12px;
            font-weight: bold;
        ''')
        header_layout.addWidget(title_label, stretch=1)
        
        layout.addLayout(header_layout)
        
        # Valor
        value_label = QLabel(str(value))
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f'''
            color: {color};
            font-size: 32px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        ''')
        layout.addWidget(value_label)
        
        self.setLayout(layout)
    
    def enterEvent(self, event):
        """Animación al pasar el mouse"""
        self.setStyleSheet(self.styleSheet().replace('scale(1.0)', 'scale(1.05)'))
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Restaurar al salir el mouse"""
        self.setStyleSheet(self.styleSheet().replace('scale(1.05)', 'scale(1.0)'))
        super().leaveEvent(event)


class AchievementBadge(QFrame):
    """Badge de logro desbloqueado"""
    
    def __init__(self, achievement, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 80)
        
        self.setStyleSheet('''
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #1a1a00, stop:1 #0a0a00);
                border: 2px solid #FFFF00;
                border-radius: 8px;
                padding: 8px;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Título del logro
        title = QLabel(achievement['title'])
        title.setStyleSheet('''
            color: #FFFF00;
            font-size: 11px;
            font-weight: bold;
        ''')
        title.setWordWrap(True)
        layout.addWidget(title)
        
        # Descripción
        desc = QLabel(achievement['description'])
        desc.setStyleSheet('''
            color: #DDDD00;
            font-size: 9px;
        ''')
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Fecha
        unlock_date = datetime.fromisoformat(achievement['unlocked_at'])
        date_str = unlock_date.strftime('%d/%m/%Y')
        date_label = QLabel(f"🔓 {date_str}")
        date_label.setStyleSheet('''
            color: #888800;
            font-size: 8px;
        ''')
        layout.addWidget(date_label)
        
        self.setLayout(layout)


class MenuPrincipalV2(QWidget):
    """Menú Principal v2 con Dashboard Mejorado"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializar gestor de estadísticas
        self.stats_manager = StatsManager()
        
        self.setup_ui()
        self.animate_entrance()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.setWindowTitle('DP-700 Training System v2.0 - Dashboard')
        self.setMinimumSize(1200, 800)
        
        # Paleta de colores Matrix
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#000000'))
        palette.setColor(QPalette.WindowText, QColor('#00FF00'))
        self.setPalette(palette)
        
        # Layout principal con scroll
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # === HEADER ===
        header = self.create_header()
        main_layout.addWidget(header)
        
        # === DASHBOARD STATS ===
        stats_section = self.create_stats_section()
        main_layout.addWidget(stats_section)
        
        # === MODOS DE ENTRENAMIENTO ===
        training_section = self.create_training_section()
        main_layout.addWidget(training_section)
        
        # === LOGROS RECIENTES ===
        achievements_section = self.create_achievements_section()
        main_layout.addWidget(achievements_section)
        
        # === FOOTER ===
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def create_header(self):
        """Crea el header principal"""
        header = QFrame()
        header.setStyleSheet('''
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #001a00, stop:0.5 #003300, stop:1 #001a00);
                border: 3px solid #00FF00;
                border-radius: 15px;
                padding: 25px;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Título principal
        title = QLabel('DP-700 TRAINING SYSTEM')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('''
            color: #00FF00;
            font-size: 36px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            text-shadow: 0 0 10px #00FF00;
        ''')
        layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel('Microsoft Fabric Data Engineer - Matrix Edition v2.0')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet('''
            color: #00DD00;
            font-size: 16px;
            font-family: 'Courier New', monospace;
        ''')
        layout.addWidget(subtitle)
        
        # ASCII Art Matrix
        ascii_art = QLabel('''
        ██████╗ ██████╗      ███████╗ ██████╗  ██████╗ 
        ██╔══██╗██╔══██╗     ╚════██║██╔═████╗██╔═████╗
        ██║  ██║██████╔╝█████╗  ██╔╝██║██╔██║██║██╔██║
        ██║  ██║██╔═══╝ ╚════╝ ██╔╝ ████╔╝██║████╔╝██║
        ██████╔╝██║           ██║   ╚██████╔╝╚██████╔╝
        ╚═════╝ ╚═╝           ╚═╝    ╚═════╝  ╚═════╝ 
        ''')
        ascii_art.setAlignment(Qt.AlignCenter)
        ascii_art.setStyleSheet('''
            color: #00FF00;
            font-size: 9px;
            font-family: 'Courier New', monospace;
            opacity: 0.7;
        ''')
        layout.addWidget(ascii_art)
        
        header.setLayout(layout)
        return header
    
    def create_stats_section(self):
        """Crea la sección de estadísticas"""
        section = QFrame()
        section.setStyleSheet('''
            QFrame {
                background: transparent;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Título de sección
        section_title = QLabel('📊 ESTADÍSTICAS GLOBALES')
        section_title.setStyleSheet('''
            color: #00FF00;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
        ''')
        layout.addWidget(section_title)
        
        # Grid de estadísticas
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        # Obtener estadísticas
        total_sessions = self.stats_manager.get_total_sessions()
        study_time = int(self.stats_manager.stats['total_study_time_minutes'])
        accuracy = self.stats_manager.get_accuracy('both')
        streak_days = self.stats_manager.get_study_streak_days()
        
        commands_completed = self.stats_manager.stats['matrix_trainer']['commands_completed']
        questions_answered = self.stats_manager.stats['module_study']['questions_answered']
        
        # Crear cards
        stats_grid.addWidget(StatCard('Sesiones Totales', total_sessions, '🎯', '#00FF00'), 0, 0)
        stats_grid.addWidget(StatCard('Tiempo de Estudio', f"{study_time}m", '⏰', '#00DD00'), 0, 1)
        stats_grid.addWidget(StatCard('Precisión Global', f"{accuracy:.1f}%", '🎯', '#FFFF00'), 0, 2)
        stats_grid.addWidget(StatCard('Racha de Días', streak_days, '🔥', '#FF8800'), 0, 3)
        
        stats_grid.addWidget(StatCard('Comandos SQL', commands_completed, '⚡', '#00FFFF'), 1, 0)
        stats_grid.addWidget(StatCard('Preguntas', questions_answered, '📚', '#FF00FF'), 1, 1)
        
        # Estadísticas de Matrix Trainer
        mt_streak = self.stats_manager.stats['matrix_trainer']['current_streak']
        mt_longest = self.stats_manager.stats['matrix_trainer']['longest_streak']
        
        stats_grid.addWidget(StatCard('Racha Actual', mt_streak, '🔥', '#00FF88'), 1, 2)
        stats_grid.addWidget(StatCard('Mejor Racha', mt_longest, '🏆', '#FFD700'), 1, 3)
        
        layout.addLayout(stats_grid)
        
        section.setLayout(layout)
        return section
    
    def create_training_section(self):
        """Crea la sección de modos de entrenamiento"""
        section = QFrame()
        section.setStyleSheet('''
            QFrame {
                background: transparent;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Título de sección
        section_title = QLabel('🎮 SELECCIONA TU MODO DE ENTRENAMIENTO')
        section_title.setStyleSheet('''
            color: #FFFF00;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
        ''')
        layout.addWidget(section_title)
        
        # === Botón Matrix Trainer Classic ===
        classic_frame = self.create_training_button(
            title='⚡ MATRIX TRAINER CLASSIC',
            description='Entrenamiento paso a paso - Escribe comandos palabra por palabra',
            detail='Modo original para memorizar sintaxis SQL secuencialmente',
            color='#00FF00',
            callback=self.launch_matrix_trainer_classic
        )
        layout.addWidget(classic_frame)
        
        # === Botón Matrix Trainer v2 (NUEVO) ===
        v2_frame = self.create_training_button(
            title='🚀 MATRIX TRAINER v2.0 - CONSOLA SQL REAL',
            description='¡NUEVO! Experiencia de consola SQL real con syntax highlighting',
            detail='Escribe comandos completos • Autocompletado • Validación en tiempo real • Historial de comandos',
            color='#00FFFF',
            callback=self.launch_matrix_trainer_v2,
            highlight=True
        )
        layout.addWidget(v2_frame)
        
        # === Botón Estudio de Módulos ===
        modules_frame = self.create_training_button(
            title='📚 MODO ESTUDIO DE MÓDULOS',
            description='Sistema de preguntas por módulos con métricas de rendimiento',
            detail='Preguntas tipo examen • Estadísticas detalladas • Modo de refuerzo',
            color='#FFFF00',
            callback=self.launch_estudio_modulos
        )
        layout.addWidget(modules_frame)
        
        section.setLayout(layout)
        return section
    
    def create_training_button(self, title, description, detail, color, callback, highlight=False):
        """Crea un botón de modo de entrenamiento"""
        frame = QFrame()
        frame.setCursor(QCursor(Qt.PointingHandCursor))
        
        border_width = '3px' if highlight else '2px'
        bg_gradient = f'''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #0a0a0a, stop:0.5 {color}22, stop:1 #0a0a0a);
        ''' if highlight else 'background: #0a0a0a;'
        
        frame.setStyleSheet(f'''
            QFrame {{
                {bg_gradient}
                border: {border_width} solid {color};
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame:hover {{
                background: {color}33;
                border: 4px solid {color};
            }}
        ''')
        
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet(f'''
            color: {color};
            font-size: 20px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        ''')
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f'''
            color: {color};
            font-size: 14px;
            padding: 5px 0;
        ''')
        layout.addWidget(desc_label)
        
        # Detalle
        detail_label = QLabel(detail)
        detail_label.setStyleSheet(f'''
            color: {color}88;
            font-size: 12px;
            font-style: italic;
        ''')
        layout.addWidget(detail_label)
        
        # Badge de "NUEVO" si está destacado
        if highlight:
            new_badge = QLabel('✨ NUEVO ✨')
            new_badge.setAlignment(Qt.AlignRight)
            new_badge.setStyleSheet(f'''
                color: {color};
                font-size: 11px;
                font-weight: bold;
                background: {color}44;
                padding: 5px 15px;
                border-radius: 15px;
            ''')
            layout.addWidget(new_badge)
        
        frame.setLayout(layout)
        
        # Conectar click
        frame.mousePressEvent = lambda event: callback()
        
        return frame
    
    def create_achievements_section(self):
        """Crea la sección de logros recientes"""
        section = QFrame()
        section.setStyleSheet('''
            QFrame {
                background: transparent;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Título de sección
        section_title = QLabel('🏆 LOGROS RECIENTES')
        section_title.setStyleSheet('''
            color: #FFFF00;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
        ''')
        layout.addWidget(section_title)
        
        # Obtener logros recientes
        achievements = self.stats_manager.get_latest_achievements(6)
        
        if achievements:
            # Grid de logros
            achievs_layout = QHBoxLayout()
            achievs_layout.setSpacing(10)
            
            for achievement in achievements:
                badge = AchievementBadge(achievement)
                achievs_layout.addWidget(badge)
            
            achievs_layout.addStretch()
            layout.addLayout(achievs_layout)
        else:
            # No hay logros aún
            no_achievs = QLabel('Comienza a entrenar para desbloquear logros 🎯')
            no_achievs.setStyleSheet('''
                color: #888888;
                font-size: 13px;
                font-style: italic;
                padding: 20px;
            ''')
            layout.addWidget(no_achievs)
        
        section.setLayout(layout)
        return section
    
    def create_footer(self):
        """Crea el footer"""
        footer = QLabel('© 2026 - DP-700 Training System v2.0 | Presiona ESC para salir')
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet('''
            color: #006600;
            font-size: 11px;
            font-family: 'Courier New', monospace;
            padding: 10px;
        ''')
        return footer
    
    def animate_entrance(self):
        """Animación de entrada"""
        # Efecto de fade-in simulado con timer
        self.setWindowOpacity(0)
        self.opacity_timer = QTimer()
        self.current_opacity = 0
        
        def increase_opacity():
            self.current_opacity += 0.1
            if self.current_opacity >= 1:
                self.opacity_timer.stop()
            self.setWindowOpacity(self.current_opacity)
        
        self.opacity_timer.timeout.connect(increase_opacity)
        self.opacity_timer.start(30)
    
    def launch_matrix_trainer_classic(self):
        """Lanza Matrix Trainer Classic"""
        try:
            subprocess.Popen([sys.executable, 'matrix_trainer.py'])
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'No se pudo lanzar Matrix Trainer Classic:\n{e}')
    
    def launch_matrix_trainer_v2(self):
        """Lanza Matrix Trainer v2"""
        try:
            subprocess.Popen([sys.executable, 'matrix_trainer_v2.py'])
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'No se pudo lanzar Matrix Trainer v2:\n{e}')
    
    def launch_estudio_modulos(self):
        """Lanza Estudio de Módulos"""
        try:
            subprocess.Popen([sys.executable, 'estudio_modulos.py'])
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'No se pudo lanzar Estudio de Módulos:\n{e}')
    
    def keyPressEvent(self, event):
        """Permite cerrar con ESC"""
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MenuPrincipalV2()
    
    # Centrar ventana
    screen = app.primaryScreen().geometry()
    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2
    window.move(x, y)
    
    window.show()
    sys.exit(app.exec_())
