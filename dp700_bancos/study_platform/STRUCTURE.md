# 📁 Estructura del Proyecto Study Platform

## 🌳 Árbol de Directorios

```
study_platform/
│
├── 📁 src/                          # Código fuente
│   ├── 📁 core/                     # Lógica de negocio
│   │   ├── data_manager.py          # Gestor de datos centralizado
│   │   ├── stats_tracker.py         # Tracking de estadísticas
│   │   ├── achievement_system.py    # Sistema de logros
│   │   └── session_manager.py       # Gestión de sesiones
│   │
│   ├── 📁 models/                   # Modelos de datos
│   │   ├── question.py              # Modelo de pregunta
│   │   ├── command.py               # Modelo de comando SQL
│   │   ├── session.py               # Modelo de sesión
│   │   ├── user_stats.py            # Estadísticas de usuario
│   │   └── achievement.py           # Modelo de logro
│   │
│   ├── 📁 services/                 # Servicios
│   │   ├── data_loader.py           # Cargador de datos
│   │   ├── persistence.py           # Persistencia JSON
│   │   └── sql_validator.py         # Validador SQL
│   │
│   ├── 📁 ui/                       # Interfaz de usuario
│   │   ├── 📁 components/           # Componentes reutilizables
│   │   │   ├── stat_card.py         # Tarjeta de estadística
│   │   │   ├── progress_ring.py     # Anillo de progreso
│   │   │   ├── achievement_badge.py # Badge de logro
│   │   │   └── modern_button.py     # Botón moderno
│   │   │
│   │   ├── 📁 views/                # Vistas principales
│   │   │   ├── dashboard_view.py    # Dashboard
│   │   │   ├── sql_trainer_view.py  # Entrenador SQL
│   │   │   ├── quiz_view.py         # Vista quiz
│   │   │   └── stats_view.py        # Estadísticas
│   │   │
│   │   └── 📁 themes/               # Temas visuales
│   │       ├── modern_light.py      # Tema claro
│   │       ├── modern_dark.py       # Tema oscuro
│   │       └── colors.py            # Paleta de colores
│   │
│   └── 📁 utils/                    # Utilidades
│       ├── constants.py             # Constantes
│       ├── helpers.py               # Funciones auxiliares
│       └── validators.py            # Validadores
│
├── 📁 data/                         # Datos de la aplicación
│   ├── 📁 questions/                # Preguntas JSON
│   ├── 📁 commands/                 # Comandos SQL JSON
│   └── 📁 achievements/             # Definición de logros
│
├── 📁 storage/                      # Datos de usuario
│   ├── user_progress.json           # Progreso
│   ├── session_history.json         # Historial
│   └── settings.json                # Configuración
│
├── 📁 assets/                       # Recursos visuales
│   ├── 📁 icons/                    # Íconos
│   ├── 📁 images/                   # Imágenes
│   └── 📁 fonts/                    # Fuentes
│
├── 📁 tests/                        # Tests unitarios
│   ├── 📁 test_core/
│   ├── 📁 test_models/
│   └── 📁 test_services/
│
├── main.py                          # Punto de entrada
├── config.py                        # Configuración global
├── requirements.txt                 # Dependencias
└── README.md                        # Documentación
```

## 📦 Descripción de Módulos

### Core (Lógica de Negocio)
- **data_manager.py**: Gestor centralizado de todos los datos
- **stats_tracker.py**: Calcula y actualiza estadísticas
- **achievement_system.py**: Verifica y desbloquea logros
- **session_manager.py**: Maneja sesiones de estudio

### Models (Estructuras de Datos)
- **question.py**: Pregunta con métricas
- **command.py**: Comando SQL con tracking
- **session.py**: Sesión de estudio
- **user_stats.py**: Estadísticas globales del usuario
- **achievement.py**: Definición de logro

### Services (Servicios)
- **data_loader.py**: Carga CSV/JSON/XML
- **persistence.py**: Guarda/carga datos de usuario
- **sql_validator.py**: Valida comandos SQL

### UI Components (Componentes Reutilizables)
- **stat_card.py**: Tarjeta de estadística animada
- **progress_ring.py**: Círculo de progreso
- **achievement_badge.py**: Badge de logro
- **modern_button.py**: Botón con efectos modernos

### UI Views (Vistas Principales)
- **dashboard_view.py**: Pantalla principal
- **sql_trainer_view.py**: Entrenador de SQL
- **quiz_view.py**: Sistema de preguntas
- **stats_view.py**: Estadísticas detalladas

### UI Themes (Temas Visuales)
- **modern_light.py**: Tema claro profesional
- **modern_dark.py**: Tema oscuro elegante
- **colors.py**: Paleta de colores centralizada

## 🎯 Flujo de Datos

```
Usuario
  ↓
main.py
  ↓
Dashboard View (UI)
  ↓
Session Manager (Core)
  ↓
Data Manager (Core)
  ↓
Models + Services
  ↓
Persistence (JSON)
```

## 🚀 Próximos Pasos

1. ✅ Estructura de carpetas creada
2. ⏳ Implementar modelos de datos
3. ⏳ Crear sistema de configuración
4. ⏳ Desarrollar componentes UI
5. ⏳ Implementar vistas principales
6. ⏳ Conectar lógica de negocio
7. ⏳ Migrar datos existentes
8. ⏳ Testing y refinamiento
