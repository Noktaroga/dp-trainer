"""
Servicio para cargar datos desde CSV y XML
"""
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict
import json

from config import Config
from src.models.question import Question, SQLCommand, DifficultyLevel


class DataLoader:
    """Carga datos desde archivos CSV y XML"""
    
    def __init__(self):
        self.questions_dir = Config.DATA_DIR / 'questions'
        self.commands_dir = Config.DATA_DIR / 'commands'
    
    def load_all_commands(self) -> List[SQLCommand]:
        """Carga todos los comandos SQL desde XML"""
        commands = []
        # Buscar recursivamente en todas las subcarpetas
        xml_files = sorted(self.commands_dir.rglob('*.xml'))
        
        for xml_file in xml_files:
            try:
                command = self.load_command_from_xml(xml_file)
                if command:
                    commands.append(command)
            except Exception as e:
                print(f"Error loading {xml_file.name}: {e}")
        
        return commands
    
    def load_command_from_xml(self, xml_path: Path) -> SQLCommand:
        """Carga un comando desde archivo XML"""
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Extraer información
        command_id = xml_path.stem
        title = root.find('title').text if root.find('title') is not None else command_id
        description = root.find('description').text if root.find('description') is not None else ""
        
        # Intentar leer el comando completo directamente del tag <full>
        full_command_element = root.find('full')
        full_command = full_command_element.text.strip() if full_command_element is not None and full_command_element.text else ""
        
        parts = []
        explanation_parts = []
        hints = []
        keywords = []
        
        for part in root.findall('.//part'):
            # Leer texto del tag hijo <text> o fallback al atributo 'text'
            text_elem = part.find('text')
            if text_elem is not None and text_elem.text:
                part_text = text_elem.text.strip()
            else:
                part_text = part.get('text', '')
            
            parts.append(part_text)
            
            # Leer descripción del tag hijo <desc> o atributo 'description'
            desc_elem = part.find('desc')
            if desc_elem is not None and desc_elem.text:
                desc = desc_elem.text.strip()
            else:
                desc = part.get('description', '')
                
            if desc:
                hints.append(desc)
            
            # Guardamos la parte con su explicación
            explanation_parts.append({
                'fragment': part_text,
                'explanation': desc
            })
            
            if part_text:
                # Añadir palabras clave relevantes de los fragmentos
                keywords.append(part_text)
        
        # Si no había tag <full>, construirlo desde las partes
        if not full_command:
            full_command = ' '.join(parts).strip()
        
        # Determinar categoría basándose en la carpeta padre
        folder_category_map = {
            'KQL': 'KQL',
            'TSQL': 'T-SQL',
            'PySpark': 'PySpark',
            'Course_Lab': 'Course Lab',
            'Fabric_Delta_Lake_Library': 'Delta Lake',
            'Fabric_Full_Lab_Library': 'Full Lab',
            'Fabric_Master_Library': 'Master Library',
            'Fabric_Spark_Analysis_Library': 'Spark Analysis',
            'Microsoft_Fabric_Command_Library': 'Fabric Commands'
        }
        
        parent_folder = xml_path.parent.name
        category = folder_category_map.get(parent_folder, self._detect_category(full_command))
        
        return SQLCommand(
            id=command_id,
            title=title,
            description=description,
            category=category,
            difficulty=DifficultyLevel.MEDIUM,
            full_command=full_command,
            hints=hints,
            keywords=keywords,
            explanation_parts=explanation_parts
        )
    
    def load_all_questions(self) -> List[Question]:
        """Carga todas las preguntas desde CSV"""
        questions = []
        csv_files = self.questions_dir.glob('dp700_*.csv')
        
        for csv_file in csv_files:
            try:
                module_questions = self.load_questions_from_csv(csv_file)
                questions.extend(module_questions)
            except Exception as e:
                print(f"Error loading {csv_file.name}: {e}")
        
        return questions
    
    def load_questions_from_csv(self, csv_path: Path) -> List[Question]:
        """Carga preguntas desde un archivo CSV con métricas"""
        questions = []
        
        # Extraer nombre del módulo del archivo
        module_name = csv_path.stem.replace('dp700_', '').replace('_', ' ').title()
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            
            for idx, row in enumerate(reader):
                try:
                    # Crear ID único
                    question_id = f"{csv_path.stem}_q{idx+1}"
                    
                    # Extraer opciones desde campo 'options' separado por ;
                    options_str = row.get('options', '')
                    if options_str:
                        options = [opt.strip() for opt in options_str.split(';') if opt.strip()]
                    else:
                        options = []
                    
                    # Respuesta correcta (puede ser múltiple: "1;2;3") -> Convertir a 0-based index
                    correct_str = row.get('correct', '1') # Default a 1 si vacío para evitar crash
                    if ';' in correct_str:
                        # Múltiples respuestas, tomar la primera
                        val = int(correct_str.split(';')[0])
                    else:
                        val = int(correct_str) if correct_str.strip().isdigit() else 1
                    
                    correct_answer = max(0, val - 1) # Asegurar >= 0
                    
                    # Explicación/notas
                    explanation = row.get('notas', row.get('second_explanation', ''))
                    
                    # PARSEAR MÉTRICAS EXISTENTES
                    metrics_str = row.get('metrics', '0;0')
                    times_correct, times_incorrect = self._parse_metrics(metrics_str)
                    times_seen = times_correct + times_incorrect
                    
                    question = Question(
                        id=question_id,
                        module=module_name,
                        section=row.get('section', 'General'),
                        difficulty=self._parse_difficulty(row.get('difficulty', 'medium')),
                        question_text=row.get('question', ''),
                        options=options,
                        correct_answer=correct_answer,
                        explanation=explanation,
                        tags=row.get('section', 'General').split(','),
                        # Métricas del CSV
                        times_seen=times_seen,
                        times_correct=times_correct,
                        times_incorrect=times_incorrect,
                        source_file=str(csv_path) # Guardamos ruta
                    )
                    
                    if not question.id: # Validar que se creó bien
                         continue
                         
                    questions.append(question)
                    
                except Exception as e:
                    print(f"Error parsing row {idx} in {csv_path}: {e}")
                    continue
        
        return questions

    def update_question_stats(self, question: Question):
        """Actualiza las métricas de una pregunta en su archivo CSV original"""
        if not question.source_file:
            print("Warning: Question has no source file!")
            return

        # Leemos todo el archivo, modificamos la línea y reescribimos
        # Esto no es eficiente para DB grandes, pero para CSV pequeños está bien
        rows = []
        target_idx = -1
        
        # El ID es "filename_q{idx}". Extraemos el índice original
        try:
            # Asumimos que el ID termina en "_q123"
            parts = question.id.split('_q')
            if len(parts) < 2: return
            target_idx = int(parts[-1]) - 1 # 0-based index del CSV original
        except:
            return

        try:
            with open(question.source_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                rows = list(reader)
            
            if 0 <= target_idx < len(rows):
                # Actualizar métricas: "correct;incorrect"
                new_metrics = f"{question.times_correct};{question.times_incorrect}"
                rows[target_idx]['metrics'] = new_metrics
                
                # Escribir de vuelta
                with open(question.source_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                    
        except Exception as e:
            print(f"Error updating stats for {question.id}: {e}")
    
    def _parse_metrics(self, metrics_str: str) -> tuple:
        """Parsea el campo metrics del CSV (formato: correcto;incorrecto)"""
        try:
            if not metrics_str or metrics_str.strip() == '':
                return (0, 0)
            
            parts = metrics_str.split(';')
            if len(parts) >= 2:
                correct = int(parts[0]) if parts[0].isdigit() else 0
                incorrect = int(parts[1]) if parts[1].isdigit() else 0
                return (correct, incorrect)
            return (0, 0)
        except:
            return (0, 0)
    
    def _detect_category(self, command: str) -> str:
        """Detecta la categoría del comando SQL"""
        command_upper = command.upper()
        
        if 'CREATE' in command_upper or 'DROP' in command_upper or 'ALTER' in command_upper:
            return 'DDL'
        elif 'INSERT' in command_upper or 'UPDATE' in command_upper or 'DELETE' in command_upper:
            return 'DML'
        elif 'SELECT' in command_upper:
            return 'DQL'
        else:
            return 'OTHER'
    
    def _parse_difficulty(self, diff_str: str) -> DifficultyLevel:
        """Parsea nivel de dificultad"""
        diff_lower = diff_str.lower()
        if 'hard' in diff_lower or 'difícil' in diff_lower:
            return DifficultyLevel.HARD
        elif 'easy' in diff_lower or 'fácil' in diff_lower:
            return DifficultyLevel.EASY
        return DifficultyLevel.MEDIUM
    
    def get_modules_summary(self) -> Dict[str, int]:
        """Retorna resumen de módulos disponibles"""
        csv_files = list(self.questions_dir.glob('dp700_*.csv'))
        summary = {}
        
        for csv_file in csv_files:
            module_name = csv_file.stem.replace('dp700_', '').replace('_', ' ').title()
            
            # Contar preguntas
            with open(csv_file, 'r', encoding='utf-8') as f:
                count = sum(1 for _ in csv.DictReader(f, delimiter=','))
            
            summary[module_name] = count
        
        return summary
    
    def calculate_questions_stats(self, questions: List[Question]) -> Dict[str, int]:
        """Calcula estadísticas agregadas de las preguntas"""
        stats = {
            'total': len(questions),
            'mastered': 0,      # >= 80% accuracy
            'learning': 0,      # 50-79% accuracy
            'new': 0,           # < 50% accuracy o nunca vistas
            'seen': 0,          # Al menos 1 intento
            'total_correct': 0,
            'total_incorrect': 0,
        }
        
        for q in questions:
            if q.times_seen == 0:
                stats['new'] += 1
            else:
                stats['seen'] += 1
                
                if q.accuracy >= 80:
                    stats['mastered'] += 1
                elif q.accuracy >= 50:
                    stats['learning'] += 1
                else:
                    stats['new'] += 1
            
            stats['total_correct'] += q.times_correct
            stats['total_incorrect'] += q.times_incorrect
        
        return stats

    def get_course_structure(self, questions: List[Question]) -> Dict[str, List[str]]:
        """Devuelve un diccionario {Modulo: [Secciones]} ordenado"""
        structure = {}
        for q in questions:
            if q.module not in structure:
                structure[q.module] = set()
            structure[q.module].add(q.section)
        
        # Convertir sets a listas ordenadas
        return {k: sorted(list(v)) for k, v in sorted(structure.items())}
