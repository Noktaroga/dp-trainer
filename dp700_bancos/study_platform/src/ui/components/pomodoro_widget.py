"""
Widget visual del Reloj Pomodoro
"""
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from ..themes.colors import ModernColors, Typography, Spacing, BorderRadius
import datetime

class PomodoroWidget(QFrame):
    """
    Componente visual del Pomodoro.
    Se comunica con el PomodoroTimer lógico.
    """
    
    # Señales para controlar la UI global
    timer_started = pyqtSignal()   # Habilitar estudio
    timer_paused = pyqtSignal()    # Deshabilitar estudio
    timer_stopped = pyqtSignal()   # Deshabilitar estudio
    
    def __init__(self, timer_logic):
        super().__init__()
        self.timer_logic = timer_logic
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        self.setProperty("frameType", "pomodoro") # Estilo especial
        self.setStyleSheet(f"""
            QFrame[frameType="pomodoro"] {{
                background-color: {ModernColors.LIGHT['bg_secondary']};
                border: 2px solid {ModernColors.LIGHT['primary']};
                border-radius: {BorderRadius.LG}px;
                padding: {Spacing.MD}px;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(Spacing.LG)
        
        # Icono / Estado
        self.icon_label = QLabel("🍅")
        self.icon_label.setStyleSheet("font-size: 24px;")
        
        # Tiempo (Grande)
        self.time_label = QLabel("27:00")
        self.time_label.setStyleSheet(f"""
            font-size: {Typography.SIZE_4XL}px;
            font-weight: {Typography.WEIGHT_BOLD};
            color: {ModernColors.LIGHT['primary']};
            font-family: monospace;
        """)
        self.time_label.setAlignment(Qt.AlignCenter)
        
        # Botones de control
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(Spacing.SM)
        
        self.btn_play = QPushButton("▶ Iniciar")
        self.btn_play.setStyleSheet(f"""
            background-color: {ModernColors.LIGHT['success']};
            color: white;
            font-weight: bold;
            padding: 8px 16px;
            border-radius: 4px;
        """)
        self.btn_play.clicked.connect(self.on_play)
        
        self.btn_pause = QPushButton("⏸ Pausar")
        self.btn_pause.setStyleSheet(f"""
            background-color: {ModernColors.LIGHT['warning']};
            color: white;
            font-weight: bold;
            padding: 8px 16px;
            border-radius: 4px;
        """)
        self.btn_pause.clicked.connect(self.on_pause)
        self.btn_pause.setVisible(False)
        
        controls_layout.addWidget(self.btn_play)
        controls_layout.addWidget(self.btn_pause)
        
        # Ensamblar
        layout.addWidget(self.icon_label)
        layout.addWidget(self.time_label)
        layout.addLayout(controls_layout)
        
        self.setLayout(layout)
        
    def connect_signals(self):
        # Conectar lógica -> UI
        self.timer_logic.tick.connect(self.update_display)
        self.timer_logic.state_changed.connect(self.update_state)
        
    def on_play(self):
        self.timer_logic.start_work()
        self.timer_started.emit()
        self.btn_play.setVisible(False)
        self.btn_pause.setVisible(True)
        
    def on_pause(self):
        self.timer_logic.pause()
        self.timer_paused.emit()
        self.btn_play.setVisible(True)
        self.btn_play.setText("▶ Reanudar")
        self.btn_pause.setVisible(False)
    
    def update_display(self, minutes, seconds, state):
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")
        
    def update_state(self, state):
        if state == "working":
            self.icon_label.setText("🍅 TRABAJO")
            self.setStyleSheet(f"""
                QFrame[frameType="pomodoro"] {{
                    background-color: {ModernColors.LIGHT['bg_secondary']};
                    border: 2px solid {ModernColors.LIGHT['success']};
                }}
            """)
        elif state == "break":
            self.icon_label.setText("☕ DESCANSO")
            self.setStyleSheet(f"""
                QFrame[frameType="pomodoro"] {{
                    background-color: {ModernColors.LIGHT['info_light']};
                    border: 2px solid {ModernColors.LIGHT['info']};
                }}
            """)
        elif state == "paused":
            self.icon_label.setText("⏸ PAUSA")
            self.setStyleSheet(f"""
                QFrame[frameType="pomodoro"] {{
                    background-color: {ModernColors.LIGHT['warning_light']};
                    border: 2px solid {ModernColors.LIGHT['warning']};
                }}
            """)
