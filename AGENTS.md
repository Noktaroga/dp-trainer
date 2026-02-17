# AGENTS.md - DP-700 Training System

Guide for AI coding agents working on this Python PyQt5 desktop application.

## Project Overview

Spanish-language training system for Microsoft Fabric Data Engineer (DP-700) certification. Built with Python 3.7+ and PyQt5. Features Matrix-themed GUI with SQL console simulator and study modules.

## Running the Application

```bash
# Install dependencies
pip install PyQt5

# Launch options (from dp700_bancos/ directory)
python launch.py                 # Quick launcher menu
python menu_principal_v2.py      # Main dashboard (RECOMMENDED)
python menu_principal.py         # Classic menu
python matrix_trainer_v2.py      # SQL console trainer
python matrix_trainer.py         # Classic trainer
python estudio_modulos.py        # Module study mode

# Console modes (from root)
python consola.py                # Console quiz
python consola_metricas.py       # Console metrics
```

## Build/Test/Lint

**No formal build system.** This is a pure Python project with no testing framework.

- No test suite exists - no `test_*.py` files found
- No linting configuration (no `pyproject.toml`, `.flake8`, etc.)
- No CI/CD pipelines
- **Manual testing only** through GUI/console interfaces

## Code Style Guidelines

### Language & Comments
- **UI strings and comments in Spanish** - maintain this convention
- Docstrings in triple quotes for classes and public methods

### Naming Conventions
- **Classes**: PascalCase (`StatsManager`, `MenuPrincipalV2`)
- **Functions/Methods**: snake_case (`load_stats()`, `check_dependencies()`)
- **Variables**: snake_case (`stats_file`, `command_history`)
- **Constants**: UPPER_CASE (`BANK_DIR`)
- **Private**: single leading underscore (`_load_stats()`)

### Imports Order
1. Standard library (`sys`, `os`, `json`, `csv`, `datetime`)
2. Third-party (`PyQt5.QtWidgets`, `PyQt5.QtGui`, `PyQt5.QtCore`)
3. Local modules (`stats_manager`, `sql_syntax_highlighter`)

### Formatting
- **4-space indentation**
- Type hints optional but encouraged (see `stats_manager.py` for reference)
- No strict line length limit observed

### PyQt5 Patterns
- Matrix theme: green (`#00FF00`) on black (`#0a0a0a`)
- Font: `'Courier New', monospace`
- Stylesheets as triple-quoted f-strings
- Use `QPalette` for theming
- Signals/slots: `clicked.connect()`, `pyqtSignal`

### Error Handling
```python
try:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error loading data: {e}")
    return default_value
```

## Project Structure

```
dp700_bancos/
├── launch.py                    # Quick launcher
├── menu_principal_v2.py         # Dashboard (main entry)
├── menu_principal.py            # Classic menu
├── matrix_trainer_v2.py         # SQL console simulator
├── matrix_trainer.py            # Classic trainer
├── estudio_modulos.py           # Study system
├── stats_manager.py             # Statistics persistence
├── sql_syntax_highlighter.py    # SQL syntax highlighting
├── command_*.xml                # 7 XML command files
├── dp700_*.csv                  # 4 CSV question banks
└── user_stats.json              # User progress (auto-generated)
```

## Data Files

- **XML**: Command definitions with tab indentation
- **CSV**: Question banks with inline metrics
- **JSON**: User statistics (`user_stats.json`) - do not delete

## Key Dependencies

- Python 3.7+
- PyQt5 (only external dependency)

## Cursor/Copilot Rules

No existing rules found in `.cursorrules`, `.cursor/rules/`, or `.github/copilot-instructions.md`.
