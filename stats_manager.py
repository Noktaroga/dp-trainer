"""
Sistema de gestión de estadísticas y progreso para DP-700 Training System
Maneja persistencia de datos, logros, y métricas de rendimiento
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class StatsManager:
    """Gestor centralizado de estadísticas y progreso del usuario"""
    
    def __init__(self, stats_file: str = 'user_stats.json'):
        self.stats_file = stats_file
        self.stats = self._load_stats()
    
    def _load_stats(self) -> dict:
        """Carga estadísticas desde archivo JSON"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error cargando estadísticas: {e}")
                return self._get_default_stats()
        return self._get_default_stats()
    
    def _get_default_stats(self) -> dict:
        """Retorna estructura de estadísticas por defecto"""
        return {
            'version': '2.0',
            'created_at': datetime.now().isoformat(),
            'last_access': datetime.now().isoformat(),
            'total_study_time_minutes': 0,
            'sessions': [],
            'matrix_trainer': {
                'commands_completed': 0,
                'total_attempts': 0,
                'total_errors': 0,
                'fastest_command_seconds': None,
                'current_streak': 0,
                'longest_streak': 0,
                'last_session': None,
                'command_history': []
            },
            'module_study': {
                'questions_answered': 0,
                'correct_answers': 0,
                'modules_completed': [],
                'current_streak': 0,
                'longest_streak': 0,
                'last_session': None
            },
            'achievements': [],
            'preferences': {
                'theme': 'matrix',  # matrix, cyberpunk, classic
                'sound_enabled': False,
                'show_hints': True,
                'auto_advance': False
            }
        }
    
    def save(self):
        """Guarda estadísticas a archivo JSON"""
        try:
            self.stats['last_access'] = datetime.now().isoformat()
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando estadísticas: {e}")
    
    def start_session(self, session_type: str) -> str:
        """Inicia una nueva sesión de estudio"""
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        session = {
            'id': session_id,
            'type': session_type,  # 'matrix_trainer' o 'module_study'
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'duration_minutes': 0,
            'stats': {}
        }
        self.stats['sessions'].append(session)
        return session_id
    
    def end_session(self, session_id: str, session_stats: dict):
        """Finaliza una sesión y actualiza estadísticas"""
        for session in self.stats['sessions']:
            if session['id'] == session_id:
                session['end_time'] = datetime.now().isoformat()
                start = datetime.fromisoformat(session['start_time'])
                end = datetime.fromisoformat(session['end_time'])
                session['duration_minutes'] = (end - start).total_seconds() / 60
                session['stats'] = session_stats
                
                # Actualizar tiempo total
                self.stats['total_study_time_minutes'] += session['duration_minutes']
                break
        
        self.save()
    
    def record_matrix_command(self, command_name: str, attempts: int, errors: int, 
                             time_seconds: float, completed: bool):
        """Registra la ejecución de un comando en Matrix Trainer"""
        mt = self.stats['matrix_trainer']
        
        if completed:
            mt['commands_completed'] += 1
            mt['current_streak'] += 1
            if mt['current_streak'] > mt['longest_streak']:
                mt['longest_streak'] = mt['current_streak']
            
            # Actualizar tiempo más rápido
            if mt['fastest_command_seconds'] is None or time_seconds < mt['fastest_command_seconds']:
                mt['fastest_command_seconds'] = time_seconds
        else:
            mt['current_streak'] = 0
        
        mt['total_attempts'] += attempts
        mt['total_errors'] += errors
        mt['last_session'] = datetime.now().isoformat()
        
        # Agregar al historial
        mt['command_history'].append({
            'command': command_name,
            'timestamp': datetime.now().isoformat(),
            'attempts': attempts,
            'errors': errors,
            'time_seconds': time_seconds,
            'completed': completed
        })
        
        # Mantener solo últimos 100 comandos
        if len(mt['command_history']) > 100:
            mt['command_history'] = mt['command_history'][-100:]
        
        self._check_achievements()
        self.save()
    
    def record_module_answer(self, module: str, question_id: str, correct: bool):
        """Registra una respuesta en el estudio de módulos"""
        ms = self.stats['module_study']
        
        ms['questions_answered'] += 1
        if correct:
            ms['correct_answers'] += 1
            ms['current_streak'] += 1
            if ms['current_streak'] > ms['longest_streak']:
                ms['longest_streak'] = ms['current_streak']
        else:
            ms['current_streak'] = 0
        
        ms['last_session'] = datetime.now().isoformat()
        
        self._check_achievements()
        self.save()
    
    def get_accuracy(self, mode: str = 'both') -> float:
        """Calcula porcentaje de aciertos"""
        if mode == 'matrix_trainer':
            mt = self.stats['matrix_trainer']
            total = mt['total_attempts']
            errors = mt['total_errors']
            if total == 0:
                return 0.0
            return ((total - errors) / total) * 100
        
        elif mode == 'module_study':
            ms = self.stats['module_study']
            if ms['questions_answered'] == 0:
                return 0.0
            return (ms['correct_answers'] / ms['questions_answered']) * 100
        
        else:  # both
            mt = self.stats['matrix_trainer']
            ms = self.stats['module_study']
            total_correct = (mt['total_attempts'] - mt['total_errors']) + ms['correct_answers']
            total_attempts = mt['total_attempts'] + ms['questions_answered']
            if total_attempts == 0:
                return 0.0
            return (total_correct / total_attempts) * 100
    
    def get_study_streak_days(self) -> int:
        """Calcula racha de días consecutivos estudiando"""
        if not self.stats['sessions']:
            return 0
        
        # Obtener fechas únicas de sesiones
        dates = set()
        for session in self.stats['sessions']:
            date = datetime.fromisoformat(session['start_time']).date()
            dates.add(date)
        
        if not dates:
            return 0
        
        sorted_dates = sorted(dates, reverse=True)
        streak = 1
        current_date = sorted_dates[0]
        
        for i in range(1, len(sorted_dates)):
            expected_date = current_date - timedelta(days=1)
            if sorted_dates[i] == expected_date:
                streak += 1
                current_date = sorted_dates[i]
            else:
                break
        
        return streak
    
    def get_total_sessions(self) -> int:
        """Retorna número total de sesiones"""
        return len(self.stats['sessions'])
    
    def get_recent_sessions(self, count: int = 5) -> List[dict]:
        """Retorna las últimas N sesiones"""
        return sorted(
            self.stats['sessions'],
            key=lambda x: x['start_time'],
            reverse=True
        )[:count]
    
    def _check_achievements(self):
        """Verifica y desbloquea logros"""
        achievements = self.stats['achievements']
        
        # Logros de Matrix Trainer
        mt = self.stats['matrix_trainer']
        self._unlock_achievement(achievements, 'first_command', 
                                 mt['commands_completed'] >= 1,
                                 '🎯 Primer Comando', 'Completaste tu primer comando SQL')
        
        self._unlock_achievement(achievements, 'command_master_10',
                                 mt['commands_completed'] >= 10,
                                 '⚡ Maestro SQL I', 'Completaste 10 comandos')
        
        self._unlock_achievement(achievements, 'command_master_50',
                                 mt['commands_completed'] >= 50,
                                 '🏆 Maestro SQL II', 'Completaste 50 comandos')
        
        self._unlock_achievement(achievements, 'perfect_streak_5',
                                 mt['current_streak'] >= 5,
                                 '🔥 Racha Perfecta', '5 comandos sin errores')
        
        self._unlock_achievement(achievements, 'speed_demon',
                                 mt['fastest_command_seconds'] is not None and 
                                 mt['fastest_command_seconds'] < 30,
                                 '⚡ Velocista', 'Comando completado en menos de 30 segundos')
        
        # Logros de Module Study
        ms = self.stats['module_study']
        self._unlock_achievement(achievements, 'first_answer',
                                 ms['questions_answered'] >= 1,
                                 '📚 Primera Respuesta', 'Respondiste tu primera pregunta')
        
        self._unlock_achievement(achievements, 'knowledge_seeker',
                                 ms['questions_answered'] >= 100,
                                 '🎓 Buscador de Conocimiento', '100 preguntas respondidas')
        
        self._unlock_achievement(achievements, 'accuracy_master',
                                 self.get_accuracy('module_study') >= 90 and 
                                 ms['questions_answered'] >= 20,
                                 '🎯 Precisión Maestra', '90% de aciertos con 20+ preguntas')
        
        # Logros generales
        self._unlock_achievement(achievements, 'dedicated_student',
                                 self.stats['total_study_time_minutes'] >= 60,
                                 '⏰ Estudiante Dedicado', '1 hora de estudio acumulada')
        
        self._unlock_achievement(achievements, 'marathon_runner',
                                 self.stats['total_study_time_minutes'] >= 600,
                                 '🏃 Maratonista', '10 horas de estudio acumuladas')
        
        self._unlock_achievement(achievements, 'consistent_learner',
                                 self.get_study_streak_days() >= 7,
                                 '📅 Aprendiz Constante', '7 días de racha de estudio')
    
    def _unlock_achievement(self, achievements: list, achievement_id: str, 
                           condition: bool, title: str, description: str):
        """Desbloquea un logro si se cumple la condición"""
        # Verificar si ya está desbloqueado
        if any(a['id'] == achievement_id for a in achievements):
            return
        
        if condition:
            achievements.append({
                'id': achievement_id,
                'title': title,
                'description': description,
                'unlocked_at': datetime.now().isoformat()
            })
    
    def get_achievements(self) -> List[dict]:
        """Retorna todos los logros desbloqueados"""
        return sorted(
            self.stats['achievements'],
            key=lambda x: x['unlocked_at'],
            reverse=True
        )
    
    def get_latest_achievements(self, count: int = 3) -> List[dict]:
        """Retorna los últimos N logros desbloqueados"""
        achievements = self.get_achievements()
        return achievements[:count]
