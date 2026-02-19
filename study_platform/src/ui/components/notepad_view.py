from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QLabel, QScrollArea, QFrame,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QColor, QFont

from ..themes.colors import ModernColors, Typography, Spacing, BorderRadius
from ...services.notes_service import NotesService
from datetime import datetime

class NoteCard(QFrame):
    """Tarjeta individual para una nota"""
    def __init__(self, timestamp: str, content: str):
        super().__init__()
        self.setProperty("frameType", "card")
        
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.SM)
        layout.setContentsMargins(Spacing.MD, Spacing.MD, Spacing.MD, Spacing.MD)
        
        # Timestamp (Pastel accent)
        try:
            # Parse ISO if needed or simplify display
            display_time = datetime.fromisoformat(timestamp).strftime("%d %b %Y - %H:%M")
        except:
            display_time = timestamp
            
        lbl_time = QLabel(f"🕒 {display_time}")
        lbl_time.setStyleSheet(f"color: {ModernColors.LIGHT['secondary']}; font-weight: {Typography.WEIGHT_BOLD}; font-size: {Typography.SIZE_XS}px;")
        layout.addWidget(lbl_time)
        
        # Content
        lbl_content = QLabel(content)
        lbl_content.setWordWrap(True)
        lbl_content.setStyleSheet(f"color: {ModernColors.LIGHT['text_primary']}; font-size: {Typography.SIZE_SM}px;")
        layout.addWidget(lbl_content)
        
        self.setLayout(layout)
        
        # Style override for cards
        self.setStyleSheet(f"""
            NoteCard {{
                background-color: {ModernColors.LIGHT['surface']};
                border: 1px solid {ModernColors.LIGHT['border']};
                border-radius: {BorderRadius.MD}px;
            }}
        """)

class NotepadView(QWidget):
    """Vista de Notas flotante integrada"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.notes_service = NotesService()
        
        # Configuración de ventana flotante
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("📝 Notas Rápidas")
        self.resize(400, 600)
        
        # Estilo base
        self.setStyleSheet(f"background-color: {ModernColors.LIGHT['bg_primary']};")
        
        self.setup_ui()
        self.load_notes()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(Spacing.MD)
        main_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Mis Anotaciones")
        title.setProperty("labelType", "subtitle")
        title.setStyleSheet(f"color: {ModernColors.LIGHT['primary']}; font-weight: bold;")
        header_layout.addWidget(title)
        
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {ModernColors.LIGHT['text_secondary']};
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {ModernColors.LIGHT['error']};
            }}
        """)
        btn_close.clicked.connect(self.hide)
        header_layout.addWidget(btn_close)
        
        main_layout.addLayout(header_layout)
        
        # Área de entrada
        input_frame = QFrame()
        input_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ModernColors.LIGHT['bg_secondary']};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.SM}px;
            }}
        """)
        input_layout = QVBoxLayout(input_frame)
        
        self.txt_input = QTextEdit()
        self.txt_input.setPlaceholderText("Escribe una nota aquí...")
        self.txt_input.setFixedHeight(80)
        self.txt_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {ModernColors.LIGHT['bg_tertiary']};
                color: {ModernColors.LIGHT['text_primary']};
                border: none;
                border-radius: {BorderRadius.SM}px;
                padding: {Spacing.SM}px;
                font-family: {Typography.FONT_FAMILY_PRIMARY};
            }}
        """)
        input_layout.addWidget(self.txt_input)
        
        btn_add = QPushButton("Agregar Nota")
        btn_add.setStyleSheet(f"""
            QPushButton {{
                background-color: {ModernColors.LIGHT['primary']};
                color: {ModernColors.LIGHT['text_inverse']};
                border-radius: {BorderRadius.SM}px;
                padding: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ModernColors.LIGHT['primary_hover']};
            }}
        """)
        btn_add.clicked.connect(self.add_note)
        input_layout.addWidget(btn_add)
        
        main_layout.addWidget(input_frame)
        
        # Lista de notas (Scroll Area)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        self.notes_container = QWidget()
        self.notes_container.setStyleSheet("background-color: transparent;")
        self.notes_layout = QVBoxLayout(self.notes_container)
        self.notes_layout.setSpacing(Spacing.MD)
        self.notes_layout.addStretch() # Empujar notas hacia arriba
        
        self.scroll_area.setWidget(self.notes_container)
        main_layout.addWidget(self.scroll_area)
        
        self.setLayout(main_layout)

    def load_notes(self):
        # Limpiar layout (excepto stretch)
        while self.notes_layout.count() > 1:
            item = self.notes_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
        notes = self.notes_service.get_notes()
        
        for note in notes:
            card = NoteCard(note['timestamp'], note['content'])
            self.notes_layout.insertWidget(self.notes_layout.count() - 1, card)

    def add_note(self):
        content = self.txt_input.toPlainText().strip()
        if content:
            self.notes_service.add_note(content)
            self.txt_input.clear()
            self.load_notes()
