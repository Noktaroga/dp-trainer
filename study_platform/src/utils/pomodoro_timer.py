"""
Controlador de Reloj Pomodoro con Detección de Foco
"""
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication
import datetime

class PomodoroState:
    INACTIVE = "inactive"
    WORKING = "working"
    BREAK = "break"
    PAUSED = "paused"

class PomodoroTimer(QObject):
    """
    Temporizador Pomodoro que solo cuenta cuando la app tiene el foco.
    - Trabajo: 27 min
    - Descanso: 9 min
    """
    
    # Señales: (minutos, segundos, estado)
    tick = pyqtSignal(int, int, str) 
    state_changed = pyqtSignal(str)
    session_finished = pyqtSignal(str) # "work" o "break" terminados
    
    WORK_TIME = 27 * 60  # 27 minutos en segundos
    BREAK_TIME = 9 * 60  # 9 minutos en segundos

    def __init__(self):
        super().__init__()
        self.state = PomodoroState.INACTIVE
        self.remaining_seconds = self.WORK_TIME
        self.total_sessions = 0
        
        # Timer principal (1 segundo)
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timeout)
        self.timer.setInterval(1000)

    def start_work(self):
        """Inicia sesión de trabajo"""
        if self.state == PomodoroState.PAUSED and self.previous_state == PomodoroState.WORKING:
            # Reanudar
            self.state = PomodoroState.WORKING
        else:
            # Nuevo inicio
            self.state = PomodoroState.WORKING
            self.remaining_seconds = self.WORK_TIME
        
        self.state_changed.emit(self.state)
        self.timer.start()

    def start_break(self):
        """Inicia descanso"""
        self.state = PomodoroState.BREAK
        self.remaining_seconds = self.BREAK_TIME
        self.state_changed.emit(self.state)
        self.timer.start()

    def pause(self):
        """Pausa el reloj y guarda estado"""
        if self.state in [PomodoroState.WORKING, PomodoroState.BREAK]:
            self.previous_state = self.state
            self.state = PomodoroState.PAUSED
            self.timer.stop()
            self.state_changed.emit(self.state)
            self.save_session_data()

    def reset(self):
        """Reinicia todo"""
        self.stop()
        self.state = PomodoroState.INACTIVE
        self.remaining_seconds = self.WORK_TIME
        self.state_changed.emit(self.state)
        # Emitir tick inicial
        m, s = divmod(self.remaining_seconds, 60)
        self.tick.emit(m, s, self.state)

    def stop(self):
        self.timer.stop()
        
    def _on_timeout(self):
        # Verificar si la ventana tiene el foco
        app = QApplication.instance()
        active_window = app.activeWindow()
        
        # Si no hay ventana activa o no es nuestra app, NO contar
        if not active_window:
            return

        # Decrementar tiempo
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            m, s = divmod(self.remaining_seconds, 60)
            self.tick.emit(m, s, self.state)
        else:
            self._finish_phase()

    def _finish_phase(self):
        self.timer.stop()
        if self.state == PomodoroState.WORKING:
            self.total_sessions += 1
            self.save_session_data() # Guardar sesión completada
            self.session_finished.emit("work")
            # Auto-iniciar descanso? O esperar usuario?
            # Según requerimiento: "si decidimos pausarlo...". Asumiré que espera confirmación o inicia descanso.
            # Por ahora, emitimos señal y pasamos a Pausa/Esperando Descanso
            self.start_break() 
            
        elif self.state == PomodoroState.BREAK:
            self.session_finished.emit("break")
            self.start_work() # Auto-loop o esperar? Loop de estudio sugiere continuidad.

    def save_session_data(self):
        """Guarda progreso (simulado por ahora, conectar a PersistenceService despues)"""
        print(f"💾 Sesión guardada: {datetime.datetime.now()} | Estado: {self.state} | Restante: {self.remaining_seconds}s")
        # Aquí llamarías a PersistenceService.save_session(duration, date...)
