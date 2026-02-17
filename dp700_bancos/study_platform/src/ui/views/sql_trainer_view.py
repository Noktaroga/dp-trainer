"""
Vista de SQL Trainer - Práctica de escritura de consultas
"""
import difflib
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QFrame, QMessageBox, QSplitter,
    QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QRegExp
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor

from ..themes.colors import ModernColors, Typography, Spacing, BorderRadius

class SQLHighlighter(QSyntaxHighlighter):
    """Resaltador de sintaxis simple para SQL"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlightingRules = []

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(ModernColors.LIGHT['primary']))
        keywordFormat.setFontWeight(Typography.WEIGHT_BOLD)
        
        keywords = [
            "SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "DROP", 
            "CREATE", "TABLE", "ALTER", "INTO", "VALUES", "AND", "OR", "NOT", 
            "NULL", "is", "AS", "distinct", "join", "on", "group", "by", "order",
            "limit", "offset", "having", "union", "all", "exists", "in", "like"
        ]
        
        for word in keywords:
            pattern = QRegExp(f"\\b{word}\\b", Qt.CaseInsensitive)
            self.highlightingRules.append((pattern, keywordFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

class SQLTrainerView(QWidget):
    """Vista para practicar comandos SQL"""
    
    back_to_dashboard = pyqtSignal()

    def __init__(self, commands, data_loader, persistence):
        super().__init__()
        self.all_commands = commands  # Store all commands
        self.commands = commands[:]   # Current playlist
        self.data_loader = data_loader
        self.persistence = persistence
        
        self.current_index = 0
        self.solved_count = 0
        self.is_random = False
        
        self.extract_categories()
        
        self.setup_ui()
        if self.commands:
            self.load_command()
        else:
            QMessageBox.warning(self, "Sin Comandos", "No se encontraron ejercicios SQL.")
            self.back_to_dashboard.emit()

    def extract_categories(self):
        """Extract unique categories from commands"""
        self.categories = sorted(list(set(cmd.category for cmd in self.all_commands)))

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(Spacing.LG)
        main_layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # --- CONTROLS SECTION ---
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(Spacing.MD)
        
        # Category Selector
        lbl_cat = QLabel("📂 Sección:")
        lbl_cat.setStyleSheet(f"font-weight: {Typography.WEIGHT_BOLD};")
        self.combo_cat = QComboBox()
        self.combo_cat.addItems(["Todas"] + self.categories)
        self.combo_cat.setFixedWidth(200)
        self.combo_cat.currentIndexChanged.connect(self.on_section_changed)
        
        # Random Toggle
        self.chk_random = QCheckBox("🔀 Modo Aleatorio")
        self.chk_random.setStyleSheet(f"font-weight: {Typography.WEIGHT_BOLD};")
        self.chk_random.stateChanged.connect(self.on_random_changed)
        
        controls_layout.addWidget(lbl_cat)
        controls_layout.addWidget(self.combo_cat)
        controls_layout.addWidget(self.chk_random)
        controls_layout.addStretch()
        
        main_layout.addLayout(controls_layout)
        
        # Contenido principal con Splitter para ajustar tamaño
        splitter = QSplitter(Qt.Horizontal)
        
        # --- PANEL IZQUIERDO (Editor) ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(Spacing.MD)
        
        # Instrucción
        self.instruction_card = QFrame()
        self.instruction_card.setProperty("frameType", "card")
        inst_layout = QVBoxLayout()
        
        self.lbl_title = QLabel("Título")
        self.lbl_title.setProperty("labelType", "subtitle")
        self.lbl_description = QLabel("Descripción...")
        self.lbl_description.setWordWrap(True)
        
        inst_layout.addWidget(self.lbl_title)
        inst_layout.addWidget(self.lbl_description)
        self.instruction_card.setLayout(inst_layout)
        left_layout.addWidget(self.instruction_card)
        
        # Editor
        lbl_editor = QLabel("✍️ Tu Consulta SQL:")
        lbl_editor.setStyleSheet(f"font-weight: {Typography.WEIGHT_BOLD};")
        left_layout.addWidget(lbl_editor)
        
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Monospace", 14))
        self.editor.setStyleSheet(f"""
            QTextEdit {{
                background-color: {ModernColors.LIGHT['bg_secondary']};
                color: {ModernColors.LIGHT['text_primary']};
                border: 1px solid {ModernColors.LIGHT['border']};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.MD}px;
                font-family: {Typography.FONT_FAMILY_MONO};
            }}
        """)
        self.highlighter = SQLHighlighter(self.editor.document())
        left_layout.addWidget(self.editor)
        
        # Botones
        actions_layout = QHBoxLayout()
        self.btn_run = QPushButton("▶ Ejecutar")
        self.btn_run.setMinimumHeight(45)
        self.btn_run.clicked.connect(self.check_solution)
        
        self.btn_hint = QPushButton("💡 Pista")
        self.btn_hint.setProperty("buttonType", "secondary")
        self.btn_hint.setMinimumHeight(45)
        self.btn_hint.clicked.connect(self.show_hint)

        self.btn_explain = QPushButton("📘 Explicación")
        self.btn_explain.setProperty("buttonType", "info") # Assuming 'info' type exists or just secondary
        self.btn_explain.setStyleSheet(f"background-color: {ModernColors.LIGHT['info']}; color: white; font-weight: bold;")
        self.btn_explain.setMinimumHeight(45)
        self.btn_explain.clicked.connect(self.show_explanation)
        
        self.btn_diff = QPushButton("🔍 Ver Diferencias")
        self.btn_diff.setProperty("buttonType", "secondary")
        self.btn_diff.setMinimumHeight(45)
        self.btn_diff.setVisible(False)
        self.btn_diff.clicked.connect(self.show_diff)
        
        self.btn_next = QPushButton("Siguiente →")
        self.btn_next.setMinimumHeight(45)
        self.btn_next.setVisible(False)
        self.btn_next.clicked.connect(self.next_command)
        
        actions_layout.addWidget(self.btn_run)
        actions_layout.addWidget(self.btn_hint)
        actions_layout.addWidget(self.btn_explain)
        actions_layout.addWidget(self.btn_diff)
        actions_layout.addWidget(self.btn_next)
        left_layout.addLayout(actions_layout)
        
        splitter.addWidget(left_widget)
        
        # --- PANEL DERECHO (Feedback) ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(Spacing.LG, 0, 0, 0)
        right_layout.setSpacing(Spacing.MD)
        
        self.feedback_frame = QFrame()
        self.feedback_frame.setVisible(False)
        feedback_inner = QVBoxLayout()
        
        self.lbl_feedback = QLabel()
        self.lbl_feedback.setWordWrap(True)
        self.lbl_feedback.setStyleSheet(f"font-size: {Typography.SIZE_LG}px; font-weight: bold;")
        feedback_inner.addWidget(self.lbl_feedback)
        
        # Solución esperada (Editor ReadOnly)
        self.lbl_expected_title = QLabel("Solución Correcta:")
        self.lbl_expected_title.setStyleSheet(f"font-weight: bold; margin-top: {Spacing.MD}px;")
        feedback_inner.addWidget(self.lbl_expected_title)
        
        self.txt_expected = QTextEdit()
        self.txt_expected.setReadOnly(True)
        self.txt_expected.setFont(QFont("Monospace", 12))
        self.txt_expected.setStyleSheet(f"""
            QTextEdit {{
                background-color: {ModernColors.LIGHT['bg_tertiary']};
                color: {ModernColors.LIGHT['text_primary']};
                border: none;
                border-radius: {BorderRadius.SM}px;
                padding: {Spacing.SM}px;
                font-family: {Typography.FONT_FAMILY_MONO};
            }}
        """)
        self.expected_highlighter = SQLHighlighter(self.txt_expected.document())
        
        feedback_inner.addWidget(self.txt_expected)
        self.feedback_frame.setLayout(feedback_inner)
        
        right_layout.addWidget(self.feedback_frame)
        right_layout.addStretch()
        
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 300]) # 2/3 ratio
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def create_header(self):
        header = QFrame()
        layout = QHBoxLayout()
        
        back_btn = QPushButton("← Volver")
        back_btn.setProperty("buttonType", "secondary")
        back_btn.clicked.connect(self.back_to_dashboard.emit)
        
        title = QLabel("💻 SQL Trainer (T-SQL & KQL)")
        title.setProperty("labelType", "title")
        
        self.lbl_progress = QLabel(f"Ejercicio 1/{len(self.commands)}") if self.commands else QLabel("0/0")
        
        layout.addWidget(back_btn)
        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.lbl_progress)
        
        header.setLayout(layout)
        return header

    def on_section_changed(self, index):
        """Handle category selection"""
        selection = self.combo_cat.currentText()
        if selection == "Todas":
            self.commands = self.all_commands[:]
        else:
            self.commands = [cmd for cmd in self.all_commands if cmd.category == selection]
            
        self.refresh_playlist()

    def on_random_changed(self, state):
        """Handle random toggle"""
        self.is_random = (state == Qt.Checked)
        self.refresh_playlist()

    def refresh_playlist(self):
        """Update playlist based on current settings"""
        if self.is_random:
            import random
            random.shuffle(self.commands)
        else:
            # Sort by ID to restore order
            self.commands.sort(key=lambda x: x.id)
            
        self.current_index = 0
        
        if self.commands:
            self.load_command()
        else:
            QMessageBox.warning(self, "Info", "No hay comandos en esta sección.")
            self.editor.clear()
            self.lbl_title.setText("-")
            self.lbl_description.setText("-")

    def load_command(self):
        if self.current_index >= len(self.commands):
            return
            
        cmd = self.commands[self.current_index]
        self.lbl_title.setText(f"{cmd.id}: {cmd.title}")
        self.lbl_description.setText(cmd.description)
        self.editor.clear()
        
        # Resetear feedback
        self.feedback_frame.setVisible(False)
        self.btn_run.setVisible(True)
        self.btn_next.setVisible(False)
        self.btn_diff.setVisible(False) 
        
        if hasattr(self, 'lbl_progress'):
            self.lbl_progress.setText(f"Ejercicio {self.current_index + 1}/{len(self.commands)}")

    def normalize_sql(self, sql):
        """Normaliza SQL para comparación (quita espacios extra, mayúsculas, signos)"""
        if not sql: return ""
        sql = sql.strip().lower()
        sql = " ".join(sql.split())
        sql = sql.replace(';', '').replace('[', '').replace(']', '')
        return sql

    def check_solution(self):
        user_sql = self.editor.toPlainText()
        cmd = self.commands[self.current_index]
        target_sql = cmd.full_command
        
        normalized_user = self.normalize_sql(user_sql)
        normalized_target = self.normalize_sql(target_sql)
        
        # Cargar estadísticas para actualizar
        stats = None
        if self.persistence:
            stats = self.persistence.load_user_stats()
            stats.sql_total_attempts += 1
        
        # Comparación directa
        if normalized_user == normalized_target:
            if stats:
                stats.sql_commands_completed += 1
                # Usar el nombre del comando como ID único
                cmd_id = cmd.id
                if cmd_id not in stats.sql_completed_ids:
                    stats.sql_completed_ids.append(cmd_id)
                
                # Manejo de racha (simple)
                stats.sql_current_streak += 1
                if stats.sql_current_streak > stats.sql_best_streak:
                    stats.sql_best_streak = stats.sql_current_streak
                    
                self.persistence.save_user_stats(stats)
                
            self.show_success(target_sql)
            return

        # Si falló, registrar error y resetear racha
        if stats:
            stats.sql_total_errors += 1
            stats.sql_current_streak = 0
            self.persistence.save_user_stats(stats)

        # Verificar keywords
        missing = []
        if cmd.keywords:
            for kw in cmd.keywords:
                if kw.lower() not in normalized_user:
                    missing.append(kw)
        
        if missing:
            self.show_error(f"Faltan palabras clave: {', '.join(missing)}", target_sql, is_hint=True)
            return
            
        # Analizar similitud
        matcher = difflib.SequenceMatcher(None, normalized_user, normalized_target)
        ratio = matcher.ratio()
        
        if ratio > 0.85:
            msg = "Casi lo tienes. Revisa pequeños detalles de sintaxis."
        elif ratio > 0.6:
            msg = "Vas por buen camino, pero hay errores en la estructura."
        else:
            msg = "La consulta es incorrecta."
            
        self.show_error(msg, target_sql)

    def show_diff(self):
        """Muestra las diferencias detalladas"""
        user_sql = self.normalize_sql(self.editor.toPlainText())
        target_sql = self.normalize_sql(self.commands[self.current_index].full_command)
        
        import difflib
        diff = difflib.ndiff(user_sql, target_sql)
        
        html = "<pre style='font-family: monospace; font-size: 14px;'>"
        for part in diff:
            code = part[0]
            char = part[2:]
            if code == ' ':
                html += f"<span style='color: {ModernColors.LIGHT['text_primary']}'>{char}</span>"
            elif code == '-':
                html += f"<span style='background-color: {ModernColors.LIGHT['error_light']}; color: {ModernColors.LIGHT['error']}; text-decoration: line-through;'>{char}</span>"
            elif code == '+':
                html += f"<span style='background-color: {ModernColors.LIGHT['success_light']}; color: {ModernColors.LIGHT['success']}; font-weight: bold;'>{char}</span>"
        html += "</pre>"
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Diferencias Detalladas")
        msg.setText("Leyenda: <span style='color:#F87171; text-decoration: line-through;'>Sobra</span> | <span style='color:#34D399; font-weight:bold;'>Falta</span>")
        msg.setInformativeText(html)
        # Hack para hacer el QMessageBox más ancho
        layout = msg.layout()
        spacer = QWidget()
        spacer.setMinimumWidth(600)
        layout.addWidget(spacer, layout.rowCount(), 0, 1, layout.columnCount())
        msg.exec_()

    def show_success(self, target_sql):
        self.feedback_frame.setVisible(True)
        self.feedback_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ModernColors.LIGHT['success_light']};
                border-left: 4px solid {ModernColors.LIGHT['success']};
                border-radius: {BorderRadius.SM}px;
                padding: {Spacing.MD}px;
            }}
        """)
        self.lbl_feedback.setText("✅ ¡Correcto! Has construido la consulta perfectamente.")
        self.lbl_expected_title.setText("Tu solución:")
        self.txt_expected.setPlainText(target_sql)
        self.txt_expected.setVisible(True)
        
        self.btn_run.setVisible(False)
        self.btn_hint.setVisible(False)
        self.btn_diff.setVisible(False)
        self.btn_next.setVisible(True)
        self.solved_count += 1

    def show_error(self, message, target_sql, is_hint=False):
        self.feedback_frame.setVisible(True)
        color_bg = ModernColors.LIGHT['warning_light'] if is_hint else ModernColors.LIGHT['error_light']
        color_border = ModernColors.LIGHT['warning'] if is_hint else ModernColors.LIGHT['error']
        
        self.feedback_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {color_bg};
                border-left: 4px solid {color_border};
                border-radius: {BorderRadius.SM}px;
                padding: {Spacing.MD}px;
            }}
        """)
        self.lbl_feedback.setText(f"{'⚠️' if is_hint else '❌'} {message}")
        self.lbl_expected_title.setText("Solución Esperada:")
        self.txt_expected.setPlainText(target_sql)
        self.txt_expected.setVisible(True)
        
        self.btn_diff.setVisible(True)

    def show_hint(self):
        cmd = self.commands[self.current_index]
        hints = cmd.hints
        if hints:
            QMessageBox.information(self, "Pista", f"💡 {hints[0]}")
        else:
            QMessageBox.information(self, "Pista", "Revisa la estructura sintáctica del comando.")

    def show_explanation(self):
        """Muestra popup con explicación detallada de cada parte"""
        cmd = self.commands[self.current_index]
        parts = cmd.explanation_parts
        
        if not parts:
            QMessageBox.information(self, "Sin Explicación", "No hay desglose detallado disponible para este comando.")
            return

        # Construir tabla HTML
        html = f"""
        <h3 style='font-family: {Typography.FONT_FAMILY_PRIMARY}; color: {ModernColors.LIGHT['primary']}'>Desglose del Comando</h3>
        <p style='font-family: {Typography.FONT_FAMILY_PRIMARY}; margin-bottom: 10px;'>Entiende cada parte de la consulta:</p>
        <table border='0' cellspacing='0' cellpadding='8' width='100%' style='border-collapse: collapse; font-family: {Typography.FONT_FAMILY_PRIMARY};'>
            <thead>
                <tr style='background-color: {ModernColors.LIGHT['bg_secondary']}; color: {ModernColors.LIGHT['text_primary']}; border-bottom: 2px solid {ModernColors.LIGHT['border']}'>
                    <th align='left' width='40%'>Fragmento de Código</th>
                    <th align='left'>Explicación</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for i, part in enumerate(parts):
            bg_color = ModernColors.LIGHT['bg_primary'] if i % 2 == 0 else ModernColors.LIGHT['bg_secondary']
            frag = part.get('fragment', '')
            expl = part.get('explanation', '')
            
            html += f"""
            <tr style='background-color: {bg_color}; border-bottom: 1px solid {ModernColors.LIGHT['border']}'>
                <td style='font-family: {Typography.FONT_FAMILY_MONO}; color: {ModernColors.LIGHT['info']}; font-weight: bold;'>{frag}</td>
                <td style='color: {ModernColors.LIGHT['text_secondary']}'>{expl}</td>
            </tr>
            """
            
        html += "</tbody></table>"
        
        # Usar QMessageBox con RichText
        msg = QMessageBox(self)
        msg.setWindowTitle(f"Explicación: {cmd.title}")
        msg.setText(html)
        msg.setTextFormat(Qt.RichText)
        
        # Ajustar tamaño
        layout = msg.layout()
        spacer = QWidget()
        spacer.setMinimumWidth(700)
        layout.addWidget(spacer, layout.rowCount(), 0, 1, layout.columnCount())
        
        msg.exec_()

    def next_command(self):
        self.current_index += 1
        if self.current_index < len(self.commands):
            self.load_command()
        else:
            QMessageBox.information(self, "¡Completado!", f"Has terminado todos los ejercicios de esta sección.\nTotal resueltos: {self.solved_count}")
            # Optional: shuffle again if in random mode to keep playing? 
            # For now, just go back.
            self.back_to_dashboard.emit()
