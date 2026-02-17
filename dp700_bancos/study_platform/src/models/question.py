"""
Modelos de datos tipificados para la aplicación
"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class DifficultyLevel(Enum):
    """Niveles de dificultad"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class MasteryLevel(Enum):
    """Niveles de dominio"""
    NEW = "new"             # < 50% accuracy
    LEARNING = "learning"   # 50-79% accuracy
    MASTERED = "mastered"   # >= 80% accuracy


@dataclass
class Question:
    """
    Modelo de pregunta con tracking de métricas
    """
    id: str
    module: str
    section: str
    difficulty: DifficultyLevel
    question_text: str
    options: List[str]
    correct_answer: int  # Índice 0-based
    explanation: str
    tags: List[str] = field(default_factory=list)
    
    # Métricas
    times_seen: int = 0
    times_correct: int = 0
    times_incorrect: int = 0
    source_file: str = "" # Ruta al archivo CSV de origen
    average_time_seconds: float = 0.0
    last_seen: Optional[str] = None  # ISO timestamp
    
    @property
    def accuracy(self) -> float:
        """Calcula el porcentaje de aciertos"""
        total = self.times_correct + self.times_incorrect
        return (self.times_correct / total * 100) if total > 0 else 0.0
    
    @property
    def mastery_level(self) -> MasteryLevel:
        """Determina el nivel de dominio"""
        if self.accuracy >= 80:
            return MasteryLevel.MASTERED
        elif self.accuracy >= 50:
            return MasteryLevel.LEARNING
        return MasteryLevel.NEW
    
    def to_dict(self) -> dict:
        """Convierte a diccionario para JSON"""
        return {
            'id': self.id,
            'module': self.module,
            'section': self.section,
            'difficulty': self.difficulty.value,
            'question_text': self.question_text,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'tags': self.tags,
            'times_seen': self.times_seen,
            'times_correct': self.times_correct,
            'times_incorrect': self.times_incorrect,
            'average_time_seconds': self.average_time_seconds,
            'last_seen': self.last_seen,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Question':
        """Crea instancia desde diccionario"""
        data['difficulty'] = DifficultyLevel(data.get('difficulty', 'medium'))
        return cls(**data)


@dataclass
class SQLCommand:
    """
    Modelo de comando SQL con tracking
    """
    id: str
    title: str
    description: str
    category: str  # DDL, DML, DQL, etc.
    difficulty: DifficultyLevel
    full_command: str
    hints: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    explanation_parts: List[dict] = field(default_factory=list)
    
    # Métricas
    attempts: int = 0
    completions: int = 0
    fastest_time_seconds: Optional[float] = None
    average_errors: float = 0.0
    last_attempted: Optional[str] = None
    
    @property
    def success_rate(self) -> float:
        """Calcula tasa de éxito"""
        return (self.completions / self.attempts * 100) if self.attempts > 0 else 0.0
    
    def to_dict(self) -> dict:
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty.value,
            'full_command': self.full_command,
            'hints': self.hints,
            'keywords': self.keywords,
            'attempts': self.attempts,
            'completions': self.completions,
            'fastest_time_seconds': self.fastest_time_seconds,
            'average_errors': self.average_errors,
            'last_attempted': self.last_attempted,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SQLCommand':
        """Crea instancia desde diccionario"""
        data['difficulty'] = DifficultyLevel(data.get('difficulty', 'medium'))
        return cls(**data)
