"""
Modelo de estadísticas de usuario
"""
from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class UserStatistics:
    """
    Estadísticas globales del usuario
    """
    # General
    total_study_time_minutes: float = 0.0
    total_sessions: int = 0
    current_streak_days: int = 0
    longest_streak_days: int = 0
    last_study_date: str = ""  # ISO date
    
    # SQL Trainer
    sql_commands_completed: int = 0
    sql_total_attempts: int = 0
    sql_total_errors: int = 0
    sql_current_streak: int = 0  # Comandos sin error
    sql_best_streak: int = 0
    sql_completed_ids: List[str] = field(default_factory=list)  # IDs únicos de comandos completados
    
    # Quiz
    quiz_questions_answered: int = 0
    quiz_correct_answers: int = 0
    quiz_current_streak: int = 0
    quiz_best_streak: int = 0
    
    # Logros
    achievements_unlocked: List[str] = field(default_factory=list)
    total_xp: int = 0
    
    # Detail Metrics per Command
    sql_command_metrics: dict = field(default_factory=dict)  # {cmd_id: {'attempts': 0, 'correct': 0, 'errors': 0}}

    @property
    def sql_accuracy(self) -> float:
        """Precisión en SQL trainer"""
        if self.sql_total_attempts == 0:
            return 0.0
        correct = self.sql_total_attempts - self.sql_total_errors
        return (correct / self.sql_total_attempts * 100)
    
    @property
    def quiz_accuracy(self) -> float:
        """Precisión en quiz"""
        if self.quiz_questions_answered == 0:
            return 0.0
        return (self.quiz_correct_answers / self.quiz_questions_answered * 100)
    
    @property
    def overall_accuracy(self) -> float:
        """Precisión global"""
        total_correct = (self.sql_total_attempts - self.sql_total_errors) + self.quiz_correct_answers
        total_attempts = self.sql_total_attempts + self.quiz_questions_answered
        return (total_correct / total_attempts * 100) if total_attempts > 0 else 0.0
    
    def to_dict(self) -> dict:
        """Convierte a diccionario para JSON"""
        return {
            'total_study_time_minutes': self.total_study_time_minutes,
            'total_sessions': self.total_sessions,
            'current_streak_days': self.current_streak_days,
            'longest_streak_days': self.longest_streak_days,
            'last_study_date': self.last_study_date,
            'sql_commands_completed': self.sql_commands_completed,
            'sql_total_attempts': self.sql_total_attempts,
            'sql_total_errors': self.sql_total_errors,
            'sql_current_streak': self.sql_current_streak,
            'sql_best_streak': self.sql_best_streak,
            'sql_command_metrics': self.sql_command_metrics, # New field
            'quiz_questions_answered': self.quiz_questions_answered,
            'quiz_correct_answers': self.quiz_correct_answers,
            'quiz_current_streak': self.quiz_current_streak,
            'quiz_best_streak': self.quiz_best_streak,
            'achievements_unlocked': self.achievements_unlocked,
            'total_xp': self.total_xp,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UserStatistics':
        """Crea instancia desde diccionario"""
        # Ensure sql_command_metrics exists if loading from old file
        if 'sql_command_metrics' not in data:
            data['sql_command_metrics'] = {}
        return cls(**data)
