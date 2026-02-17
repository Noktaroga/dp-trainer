"""
Servicio de persistencia de datos de usuario
"""
import json
from pathlib import Path
from typing import Optional

from config import Config
from src.models.user_stats import UserStatistics


class PersistenceService:
    """Maneja la persistencia de datos de usuario"""
    
    def __init__(self):
        self.user_stats_file = Config.STORAGE_DIR / 'user_progress.json'
        self.ensure_storage()
    
    def ensure_storage(self):
        """Asegura que el directorio de storage exista"""
        Config.STORAGE_DIR.mkdir(exist_ok=True)
    
    def load_user_stats(self) -> UserStatistics:
        """Carga estadísticas de usuario"""
        if self.user_stats_file.exists():
            try:
                with open(self.user_stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return UserStatistics.from_dict(data)
            except Exception as e:
                print(f"Error loading user stats: {e}")
                return UserStatistics()
        
        return UserStatistics()
    
    def save_user_stats(self, stats: UserStatistics):
        """Guarda estadísticas de usuario"""
        try:
            with open(self.user_stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving user stats: {e}")
    
    def migrate_old_stats(self, old_stats_path: Path) -> Optional[UserStatistics]:
        """Migra estadísticas del sistema anterior"""
        if not old_stats_path.exists():
            return None
        
        try:
            with open(old_stats_path, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
            
            # Mapear datos antiguos al nuevo formato
            stats = UserStatistics()
            
            # Mapeo de campos (adaptable según tu formato anterior)
            stats.total_study_time_minutes = old_data.get('global_stats', {}).get('total_study_time_minutes', 0)
            stats.total_sessions = old_data.get('global_stats', {}).get('total_sessions', 0)
            stats.current_streak_days = old_data.get('achievements', {}).get('current_streak', 0)
            
            # SQL Trainer
            matrix_stats = old_data.get('matrix_trainer', {})
            stats.sql_commands_completed = matrix_stats.get('commands_completed', 0)
            stats.sql_total_attempts = matrix_stats.get('total_attempts', 0)
            stats.sql_total_errors = matrix_stats.get('total_errors', 0)
            stats.sql_best_streak = matrix_stats.get('best_streak', 0)
            
            # Module Study
            module_stats = old_data.get('module_study', {})
            stats.quiz_questions_answered = module_stats.get('total_answered', 0)
            stats.quiz_correct_answers = module_stats.get('correct_answers', 0)
            
            # Achievements
            stats.achievements_unlocked = old_data.get('achievements', {}).get('unlocked', [])
            
            return stats
            
        except Exception as e:
            print(f"Error migrating old stats: {e}")
            return None
