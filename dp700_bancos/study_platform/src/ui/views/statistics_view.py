"""
Vista de Estadísticas Detalladas
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QScrollArea, QProgressBar, QGridLayout,
    QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from ..themes.colors import ModernColors, Typography, Spacing, BorderRadius

class ModuleProgressCard(QFrame):
    """Tarjeta de progreso para un módulo específico"""
    def __init__(self, module_name, stats):
        super().__init__()
        self.setProperty("frameType", "card")
        self.setup_ui(module_name, stats)

    def setup_ui(self, module_name, stats):
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.SM)
        
        # Título del módulo y %
        header_layout = QHBoxLayout()
        title = QLabel(module_name)
        title.setProperty("labelType", "subtitle")
        title.setWordWrap(True)
        
        percent_val = stats['accuracy']
        percent = QLabel(f"{percent_val:.1f}%")
        percent.setStyleSheet(f"""
            font-size: {Typography.SIZE_XL}px;
            font-weight: bold;
            color: {self.get_color_by_score(percent_val)};
        """)
        
        header_layout.addWidget(title, 1)
        header_layout.addWidget(percent)
        layout.addLayout(header_layout)
        
        # Barra de progreso visual
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setValue(int(percent_val))
        progress.setTextVisible(False)
        progress.setFixedHeight(10)
        progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: {ModernColors.LIGHT['bg_tertiary']};
                border-radius: 5px;
            }}
            QProgressBar::chunk {{
                background-color: {self.get_color_by_score(percent_val)};
                border-radius: 5px;
            }}
        """)
        layout.addWidget(progress)
        
        # Detalles numéricos
        details = QLabel(f"Vistas: {stats['seen']}/{stats['total']} | Masterizadas: {stats['mastered']}")
        details.setProperty("labelType", "caption")
        layout.addWidget(details)
        
        self.setLayout(layout)

    def get_color_by_score(self, score):
        if score >= 80: return ModernColors.LIGHT['success']
        if score >= 50: return ModernColors.LIGHT['warning']
        return ModernColors.LIGHT['error']

class StatisticsView(QWidget):
    """Vista principal de estadísticas"""
    
    back_to_dashboard = pyqtSignal()

    def __init__(self, questions, user_stats, persistence, commands=None):
        super().__init__()
        self.questions = questions
        self.user_stats = user_stats
        self.persistence = persistence
        self.commands = commands or []
        
        self.calculate_stats()
        self.setup_ui()

    def calculate_stats(self):
        """Calcula estadísticas desglosadas por módulo"""
        self.module_stats = {}
        
        for q in self.questions:
            if q.module not in self.module_stats:
                self.module_stats[q.module] = {
                    'total': 0, 'seen': 0, 'mastered': 0, 
                    'correct': 0, 'incorrect': 0
                }
            
            m = self.module_stats[q.module]
            m['total'] += 1
            if q.times_seen > 0:
                m['seen'] += 1
                m['correct'] += q.times_correct
                m['incorrect'] += q.times_incorrect
                if q.accuracy >= 80:
                    m['mastered'] += 1

        # Calcular porcentajes finales
        for m in self.module_stats.values():
            total_attempts = m['correct'] + m['incorrect']
            m['accuracy'] = (m['correct'] / total_attempts * 100) if total_attempts > 0 else 0.0

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(Spacing.LG)
        main_layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(Spacing.XL)
        
        # 1. Resumen Global (Tarjetas grandes)
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(Spacing.LG)
        
        # Calcular totales globales para mostrar (basados en preguntas reales)
        total_questions = len(self.questions)
        total_seen = sum(1 for q in self.questions if q.times_seen > 0)
        total_mastered = sum(1 for q in self.questions if q.accuracy >= 80 and q.times_seen > 0)
        
        # Tarjeta 1: Cobertura
        card_coverage = self.create_stat_card("Cobertura del Curso", 
                                            f"{total_seen}/{total_questions}", 
                                            f"{int(total_seen/total_questions*100)}% Completado")
        summary_layout.addWidget(card_coverage)
        
        # Tarjeta 2: Dominio
        mastery_pct = int(total_mastered/total_seen * 100) if total_seen > 0 else 0
        card_mastery = self.create_stat_card("Nivel de Maestría", 
                                           f"{total_mastered}", 
                                           f"{mastery_pct}% de lo estudiado es Master")
        summary_layout.addWidget(card_mastery)
        
        # Tarjeta 3: Tiempo (Fake por ahora o real de user_stats)
        # Asumimos que user_stats tiene el dato real acumulado
        hours = int(self.user_stats.total_study_time_minutes // 60)
        mins = int(self.user_stats.total_study_time_minutes % 60)
        card_time = self.create_stat_card("Tiempo Total", 
                                        f"{hours}h {mins}m", 
                                        "Invertido estudiando")
        summary_layout.addWidget(card_time)
        
        content_layout.addLayout(summary_layout)
        
        # ---------------------------------------------------------
        # 2. Estadísticas de Comandos SQL/KQL
        if self.commands:
            lbl_sql = QLabel("Entrenamiento SQL/KQL")
            lbl_sql.setProperty("labelType", "subtitle")
            content_layout.addWidget(lbl_sql)
            
            sql_layout = QHBoxLayout()
            sql_layout.setSpacing(Spacing.LG)
            
            # Datos de SQL
            total_cmds = len(self.commands)
            completed_unique = len(self.user_stats.sql_completed_ids)
            pct_completed = int((completed_unique / total_cmds * 100)) if total_cmds > 0 else 0
            
            # Tarjeta Progreso Comandos
            card_sql_prog = self.create_stat_card("Progreso Comandos",
                                                f"{completed_unique}/{total_cmds}",
                                                f"{pct_completed}% Completado")
            
            # Tarjeta Precisión SQL
            accuracy = self.user_stats.sql_accuracy
            card_sql_acc = self.create_stat_card("Precisión SQL",
                                               f"{accuracy:.1f}%",
                                               f"En {self.user_stats.sql_total_attempts} intentos")
            
            # Tarjeta Racha
            streak = self.user_stats.sql_best_streak
            card_sql_streak = self.create_stat_card("Mejor Racha",
                                                  f"{streak} 🔥",
                                                  "Comandos seguidos sin error")
            
            sql_layout.addWidget(card_sql_prog)
            sql_layout.addWidget(card_sql_acc)
            sql_layout.addWidget(card_sql_streak)
            
            content_layout.addLayout(sql_layout)
            
            # --- Weakest Commands Section ---
            lbl_weak = QLabel("⚡ Comandos que requieren atención (Menor precisión)")
            lbl_weak.setProperty("labelType", "subtitle")
            content_layout.addWidget(lbl_weak)
            
            weak_layout = QVBoxLayout()
            weak_layout.setSpacing(Spacing.SM)
            
            # Helper to get command by ID
            cmd_map = {str(c.id): c for c in self.commands}
            
            # Calculate metrics list
            metrics_list = []
            for cmd_id, m in self.user_stats.sql_command_metrics.items():
                if m['attempts'] > 0:
                    acc = (m['correct'] / m['attempts']) * 100
                    cmd_obj = cmd_map.get(str(cmd_id))
                    title = cmd_obj.title if cmd_obj else f"Command {cmd_id}"
                    metrics_list.append({
                        'id': cmd_id,
                        'title': title,
                        'accuracy': acc,
                        'attempts': m['attempts'],
                        'correct': m['correct']
                    })
            
            # Sort: lowest accuracy first, then highest attempts (prioritize identifying consistent failures)
            metrics_list.sort(key=lambda x: (x['accuracy'], -x['attempts']))
            
            top_weak = metrics_list[:5]
            
            if not top_weak:
                lbl_no_data = QLabel("No hay suficientes datos. ¡Sigue practicando!")
                lbl_no_data.setStyleSheet(f"color: {ModernColors.LIGHT['text_secondary']}; font-style: italic;")
                weak_layout.addWidget(lbl_no_data)
            else:
                for item in top_weak:
                    row_frame = QFrame()
                    row_frame.setStyleSheet(f"""
                        background-color: {ModernColors.LIGHT['bg_secondary']};
                        border-radius: {BorderRadius.SM}px;
                        padding: {Spacing.SM}px;
                    """)
                    row_layout = QHBoxLayout(row_frame)
                    
                    lbl_name = QLabel(f"<b>{item['title']}</b>")
                    lbl_stats = QLabel(f"Precisión: <span style='color:{ModernColors.LIGHT['error']}'>{item['accuracy']:.1f}%</span> ({item['correct']}/{item['attempts']})")
                    
                    row_layout.addWidget(lbl_name, 1)
                    row_layout.addWidget(lbl_stats)
                    weak_layout.addWidget(row_frame)
            
            content_layout.addLayout(weak_layout)
        # ---------------------------------------------------------

        # 3. Desglose por Módulo
        lbl_modules = QLabel("Desglose por Módulo")
        lbl_modules.setProperty("labelType", "subtitle")
        content_layout.addWidget(lbl_modules)
        
        modules_grid = QGridLayout()
        modules_grid.setSpacing(Spacing.LG)
        
        row, col = 0, 0
        for module_name, stats in self.module_stats.items():
            card = ModuleProgressCard(module_name, stats)
            modules_grid.addWidget(card, row, col)
            col += 1
            if col > 1: # 2 columnas
                col = 0
                row += 1
        
        content_layout.addLayout(modules_grid)
        content_layout.addStretch()
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)

    def create_header(self):
        header = QFrame()
        layout = QHBoxLayout()
        
        back_btn = QPushButton("← Volver")
        back_btn.setProperty("buttonType", "secondary")
        back_btn.clicked.connect(self.back_to_dashboard.emit)
        
        title = QLabel("📈 Estadísticas Detalladas")
        title.setProperty("labelType", "title")
        
        layout.addWidget(back_btn)
        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        dummy = QWidget()
        dummy.setFixedWidth(back_btn.sizeHint().width())
        layout.addWidget(dummy)
        
        header.setLayout(layout)
        return header

    def create_stat_card(self, title, value, subtitle):
        frame = QFrame()
        frame.setProperty("frameType", "elevated")
        layout = QVBoxLayout()
        
        lbl_title = QLabel(title)
        lbl_title.setProperty("labelType", "caption")
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet(f"""
            font-size: {Typography.SIZE_4XL}px;
            font-weight: bold;
            color: {ModernColors.LIGHT['primary']};
        """)
        
        lbl_sub = QLabel(subtitle)
        lbl_sub.setProperty("labelType", "caption")
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        layout.addWidget(lbl_sub)
        frame.setLayout(layout)
        return frame
