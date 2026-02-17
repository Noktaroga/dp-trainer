"""
Tema moderno claro - Profesional y altamente legible
"""
from .colors import ModernColors, Typography, Spacing, BorderRadius

class ModernLightTheme:
    """Tema claro moderno con excelente legibilidad"""
    
    def __init__(self):
        self.colors = ModernColors.LIGHT
        
    def get_stylesheet(self) -> str:
        """Retorna el stylesheet completo de PyQt5"""
        
        c = self.colors
        
        return f"""
        /* ===== ESTILOS GLOBALES ===== */
        QWidget {{
            background-color: {c['bg_secondary']};
            color: {c['text_primary']};
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: {Typography.SIZE_BASE}px;
        }}
        
        /* ===== VENTANA PRINCIPAL ===== */
        QMainWindow {{
            background-color: {c['bg_secondary']};
        }}
        
        /* ===== BOTONES MODERNOS ===== */
        QPushButton {{
            background-color: {c['primary']};
            color: {c['text_inverse']};
            border: none;
            border-radius: {BorderRadius.MD}px;
            padding: {Spacing.MD}px {Spacing.LG}px;
            font-size: {Typography.SIZE_BASE}px;
            font-weight: {Typography.WEIGHT_MEDIUM};
            min-height: 44px;
        }}
        
        QPushButton:hover {{
            background-color: {c['primary_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {c['primary_hover']};
            padding-top: {Spacing.MD + 1}px;
        }}
        
        QPushButton:disabled {{
            background-color: {c['bg_tertiary']};
            color: {c['text_tertiary']};
        }}
        
        /* Botón secundario */
        QPushButton[buttonType="secondary"] {{
            background-color: transparent;
            color: {c['primary']};
            border: 2px solid {c['primary']};
        }}
        
        QPushButton[buttonType="secondary"]:hover {{
            background-color: {c['primary_light']};
        }}
        
        /* ===== LABELS ===== */
        QLabel {{
            background-color: transparent;
            color: {c['text_primary']};
        }}
        
        QLabel[labelType="title"] {{
            font-size: {Typography.SIZE_3XL}px;
            font-weight: {Typography.WEIGHT_BOLD};
            color: {c['text_primary']};
        }}
        
        QLabel[labelType="subtitle"] {{
            font-size: {Typography.SIZE_XL}px;
            font-weight: {Typography.WEIGHT_SEMIBOLD};
            color: {c['text_primary']};
        }}
        
        QLabel[labelType="caption"] {{
            font-size: {Typography.SIZE_SM}px;
            color: {c['text_secondary']};
        }}
        
        /* ===== FRAMES Y TARJETAS ===== */
        QFrame[frameType="card"] {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
            border-radius: {BorderRadius.LG}px;
            padding: {Spacing.LG}px;
        }}
        
        QFrame[frameType="elevated"] {{
            background-color: {c['surface_elevated']};
            border: none;
            border-radius: {BorderRadius.LG}px;
        }}
        
        /* ===== SCROLLBAR MODERNA ===== */
        QScrollBar:vertical {{
            border: none;
            background: {c['bg_tertiary']};
            width: 8px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {c['border_hover']};
            border-radius: 4px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {c['text_tertiary']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* ===== PROGRESS BAR ===== */
        QProgressBar {{
            border: none;
            border-radius: {BorderRadius.SM}px;
            background-color: {c['bg_tertiary']};
            text-align: center;
            color: {c['text_primary']};
            font-weight: {Typography.WEIGHT_MEDIUM};
            height: 24px;
        }}
        
        QProgressBar::chunk {{
            border-radius: {BorderRadius.SM}px;
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 {c['primary']},
                stop: 1 {c['secondary']}
            );
        }}
        
        /* ===== TEXT EDIT (para SQL) ===== */
        QTextEdit, QPlainTextEdit {{
            background-color: {c['surface']};
            border: 2px solid {c['border']};
            border-radius: {BorderRadius.MD}px;
            padding: {Spacing.MD}px;
            color: {c['text_primary']};
            font-family: 'JetBrains Mono', monospace;
            font-size: {Typography.SIZE_BASE}px;
            selection-background-color: {c['primary_light']};
        }}
        
        QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {c['primary']};
        }}
        
        /* ===== COMBO BOX ===== */
        QComboBox {{
            background-color: {c['surface']};
            border: 2px solid {c['border']};
            border-radius: {BorderRadius.MD}px;
            padding: {Spacing.SM}px {Spacing.MD}px;
            color: {c['text_primary']};
            min-height: 36px;
        }}
        
        QComboBox:hover {{
            border-color: {c['border_hover']};
        }}
        
        QComboBox:focus {{
            border-color: {c['primary']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {c['text_secondary']};
            margin-right: 10px;
        }}
        
        /* ===== TAB WIDGET ===== */
        QTabWidget::pane {{
            border: 1px solid {c['border']};
            border-radius: {BorderRadius.MD}px;
            background-color: {c['surface']};
            padding: {Spacing.MD}px;
        }}
        
        QTabBar::tab {{
            background-color: transparent;
            color: {c['text_secondary']};
            padding: {Spacing.MD}px {Spacing.LG}px;
            border: none;
            border-bottom: 3px solid transparent;
            font-weight: {Typography.WEIGHT_MEDIUM};
        }}
        
        QTabBar::tab:selected {{
            color: {c['primary']};
            border-bottom-color: {c['primary']};
        }}
        
        QTabBar::tab:hover {{
            color: {c['text_primary']};
        }}
        
        /* ===== RADIO BUTTON ===== */
        QRadioButton {{
            spacing: {Spacing.SM}px;
            color: {c['text_primary']};
        }}
        
        QRadioButton::indicator {{
            width: 20px;
            height: 20px;
            border-radius: 10px;
            border: 2px solid {c['border_hover']};
        }}
        
        QRadioButton::indicator:checked {{
            background-color: {c['primary']};
            border-color: {c['primary']};
        }}
        
        /* ===== TOOLTIPS ===== */
        QToolTip {{
            background-color: {c['text_primary']};
            color: {c['text_inverse']};
            border: none;
            border-radius: {BorderRadius.SM}px;
            padding: {Spacing.SM}px {Spacing.MD}px;
            font-size: {Typography.SIZE_SM}px;
        }}
        """
