# DP-700 Training System v2.0 - Matrix Edition

Sistema de entrenamiento premium para la certificación Microsoft Fabric Data Engineer (DP-700) con experiencia de consola SQL real, estadísticas avanzadas y gamificación.

## 🌟 Características Principales

### 🎮 Tres Modos de Entrenamiento

1. **Matrix Trainer Classic** - Entrenamiento paso a paso
   - Aprende comandos SQL palabra por palabra
   - Sistema de errores y progreso
   - Perfecto para memorizar sintaxis

2. **Matrix Trainer v2.0** - ⚡ Experiencia de Consola SQL Real (NUEVO)
   - Editor SQL con syntax highlighting en tiempo real
   - Autocompletado inteligente (Ctrl+Space)
   - Validación completa de comandos (F5 o Ctrl+Enter)
   - Historial de comandos (Ctrl+↑/↓)
   - Modo guiado vs modo libre
   - Pistas contextuales mientras escribes

3. **Estudio de Módulos** - Sistema de preguntas tipo examen
   - Preguntas por módulos y secciones
   - Métricas de rendimiento detalladas
   - Sistema de dominio adaptativo
   - Práctica personalizada por categoría

### 📊 Sistema de Estadísticas Persistente

- **Tracking Global**: Todas tus sesiones se guardan automáticamente
- **Métricas Detalladas**: 
  - Tiempo de estudio total
  - Racha de días consecutivos
  - Precisión global y por modo
  - Comandos completados
  - Preguntas respondidas

### 🏆 Sistema de Logros

Desbloquea logros mientras estudias:
- 🎯 Primer Comando
- ⚡ Maestro SQL I/II
- 🔥 Racha Perfecta
- ⚡ Velocista
- 📚 Primera Respuesta
- 🎓 Buscador de Conocimiento
- 🎯 Precisión Maestra
- ⏰ Estudiante Dedicado
- 🏃 Maratonista
- 📅 Aprendiz Constante

### 🎨 Diseño Premium

- **Estética Matrix**: Verde sobre negro, tipografía monospace
- **Animaciones sutiles**: Transiciones suaves y feedback visual
- **Dashboard Rico**: Tarjetas estadísticas, barras de progreso animadas
- **Responsive**: Interfaz adaptable que aprovecha toda la pantalla

## 📋 Requisitos

- Python 3.7+
- PyQt5

## 🚀 Instalación

1. Instalar dependencias:
```bash
pip install PyQt5
```

2. Asegurarse de tener los archivos de comandos XML y módulos CSV en el directorio del proyecto

## 💻 Uso

### Iniciar el Sistema

**Opción 1: Menú Principal v2 (Recomendado)**
```bash
python menu_principal_v2.py
```

**Opción 2: Menú Principal Classic**
```bash
python menu_principal.py
```

### Modos Individuales

**Matrix Trainer Classic:**
```bash
python matrix_trainer.py
```

**Matrix Trainer v2 (Consola SQL Real):**
```bash
python matrix_trainer_v2.py
```

**Estudio de Módulos:**
```bash
python estudio_modulos.py
```

## 🎯 Atajos de Teclado

### Matrix Trainer v2 (Consola SQL)
- `F5` o `Ctrl+Enter`: Ejecutar/validar comando
- `Ctrl+Space`: Mostrar autocompletado
- `Ctrl+↑`: Comando anterior del historial
- `Ctrl+↓`: Comando siguiente del historial

### General
- `ESC`: Cerrar ventana

## 📁 Estructura de Archivos

```
dp700_bancos/
├── menu_principal_v2.py          # Menú principal mejorado con dashboard
├── menu_principal.py              # Menú principal classic
├── matrix_trainer_v2.py           # Matrix Trainer v2 - Consola SQL real
├── matrix_trainer.py              # Matrix Trainer classic
├── estudio_modulos.py             # Sistema de estudio de módulos
├── stats_manager.py               # Gestor de estadísticas persistente
├── sql_syntax_highlighter.py     # Syntax highlighter SQL
├── command_*.xml                  # Archivos de comandos SQL
├── dp700_*.csv                    # Archivos de preguntas por módulo
└── user_stats.json               # Estadísticas del usuario (generado automáticamente)
```

## 📊 Archivos de Configuración

### user_stats.json
Archivo generado automáticamente que contiene:
- Estadísticas globales de progreso
- Historial de sesiones
- Logros desbloqueados
- Preferencias del usuario

**No eliminar este archivo** - contiene todo tu progreso.

## 🎓 Tips de Estudio

### Matrix Trainer v2
1. **Modo Guiado**: Recibe pistas específicas sobre errores
2. **Modo Libre**: Practica sin ayuda para simular el examen real
3. Usa el autocompletado para descubrir funciones SQL
4. Revisa el historial para ver tus comandos anteriores

### Estudio de Módulos
1. Revisa las estadísticas de dominio antes de empezar
2. Usa las categorías clickeables para ver preguntas específicas
3. Practica las preguntas "Nuevas" primero
4. Refuerza las preguntas marcadas como "Practicar"
5. Las preguntas "Dominadas" son para repaso ocasional

## 🆕 Novedades v2.0

### Dashboard Mejorado
- Tarjetas estadísticas animadas
- Visualización de logros recientes
- Accesos rápidos a sesiones
- Progreso visual en tiempo real

### Matrix Trainer v2
- **Editor SQL completo** en lugar de palabra por palabra
- **Syntax highlighting** con colores personalizables
- **Autocompletado** de palabras clave SQL
- **Validación completa** del comando
- **Historial** navegable de comandos

### Sistema de Estadísticas
- Tracking automático de todas las sesiones
- Cálculo de rachas diarias
- Métricas de velocidad y precisión
- Persistencia automática

### Sistema de Logros
- 10+ logros desbloqueables
- Notificaciones visuales
- Tracking de progreso

## 🔧 Personalización

### Temas (próximamente)
El sistema soportará temas adicionales:
- Matrix (actual)
- Cyberpunk
- Classic

## 🐛 Solución de Problemas

**Error: ModuleNotFoundError: No module named 'PyQt5'**
```bash
pip install PyQt5
```

**Las estadísticas no se guardan:**
- Verifica que tienes permisos de escritura en el directorio
- Asegúrate de cerrar las aplicaciones correctamente (no forzar cierre)

**El syntax highlighting no funciona:**
- Verifica que `sql_syntax_highlighter.py` está en el mismo directorio
- Reinicia la aplicación

## 📝 Notas

- Las estadísticas se guardan automáticamente
- Cada sesión se registra individualmente
- Los logros se desbloquean en tiempo real
- El progreso es acumulativo entre sesiones

## 🎯 Roadmap

- [ ] Modo examen completo con temporizador
- [ ] Exportar estadísticas a PDF
- [ ] Sincronización en la nube
- [ ] Más temas visuales
- [ ] Modo colaborativo

## 📜 Licencia

© 2026 - Sistema de Entrenamiento DP-700

---

**¡Buena suerte con tu certificación DP-700!** 🚀
