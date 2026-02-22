from pathlib import Path

class Config:
    """Configuración centralizada de la aplicación"""
    
    # Rutas base
    BASE_DIR = Path(__file__).parent
    SRC_DIR = BASE_DIR / 'src'
    DATA_DIR = BASE_DIR / 'data'
    STORAGE_DIR = BASE_DIR / 'storage'
    ASSETS_DIR = BASE_DIR / 'assets'
    
    # Configuración de ventana
    WINDOW_TITLE = "DP-700 Study Platform"
    WINDOW_MIN_WIDTH = 1200
    WINDOW_MIN_HEIGHT = 800
    
    # Animaciones
    ANIMATION_DURATION = 200  # ms
    
    # Umbrales de estudio
    MASTERY_THRESHOLD = 80  # % para considerar dominado
    LEARNING_THRESHOLD = 50  # % para en aprendizaje
    
    # Límites
    MAX_ERRORS_PER_COMMAND = 3
    RECENT_ACHIEVEMENTS_COUNT = 6
    
    # Tema por defecto
    DEFAULT_THEME = 'light'  # 'light' o 'dark'
    
    @classmethod
    def ensure_directories(cls):
        """Crea directorios necesarios si no existen"""
        cls.STORAGE_DIR.mkdir(exist_ok=True)
        (cls.DATA_DIR / 'questions').mkdir(parents=True, exist_ok=True)
        (cls.DATA_DIR / 'commands').mkdir(parents=True, exist_ok=True)
        (cls.DATA_DIR / 'achievements').mkdir(parents=True, exist_ok=True)
