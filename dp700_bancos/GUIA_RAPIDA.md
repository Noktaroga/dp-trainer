# 🚀 Guía Rápida - DP-700 Training System v2.0

## ⚡ Inicio Rápido

### Lanzar el Sistema
```bash
python3 launch.py
```
O, para ir directo al dashboard:
```bash
python3 menu_principal_v2.py
```

---

## 🎮 Modos de Entrenamiento

### 1. Matrix Trainer v2.0 - Consola SQL Real ⚡ (NUEVO)

**¿Qué es?**
Una experiencia de consola SQL real donde escribes comandos completos con ayudas inteligentes.

**¿Cuándo usarlo?**
- Cuando quieres practicar como si estuvieras en SSMS o SQL Server
- Para acostumbrarte a escribir comandos completos
- Si ya conoces la sintaxis y quieres validación completa

**Características:**
- ✅ Syntax highlighting en tiempo real
- ✅ Autocompletado (Ctrl+Space)
- ✅ Historial de comandos (Ctrl+↑/↓)
- ✅ Validación completa (F5)
- ✅ Modo guiado con pistas

**Atajos:**
- `F5` o `Ctrl+Enter` → Ejecutar comando
- `Ctrl+Space` → Autocompletar
- `Ctrl+↑` → Comando anterior
- `Ctrl+↓` → Comando siguiente

---

### 2. Matrix Trainer Classic 📝

**¿Qué es?**
Entrenamiento paso a paso donde escribes comandos palabra por palabra.

**¿Cuándo usarlo?**
- Cuando estás empezando con SQL
- Para memorizar sintaxis exacta
- Si quieres ir lento y seguro

**Características:**
- ✅ Entrenamiento secuencial
- ✅ Pistas por cada palabra
- ✅ Sistema de errores limitado
- ✅ Progreso visual

---

### 3. Estudio de Módulos 📚

**¿Qué es?**
Sistema de preguntas tipo examen con métricas de rendimiento.

**¿Cuándo usarlo?**
- Para prepararte para el examen de certificación
- Cuando quieres practicar conceptos teóricos
- Para repasar módulos específicos

**Características:**
- ✅ Preguntas por módulo y sección
- ✅ Estadísticas de dominio
- ✅ Práctica personalizada
- ✅ Métricas detalladas

**Tips:**
1. Revisa el panel de dominio antes de empezar
2. Click en las categorías para ver preguntas específicas
3. Practica primero las "Nuevas"
4. Refuerza las de "Practicar"

---

## 📊 Dashboard y Estadísticas

### Interpretar el Dashboard

**Tarjetas Estadísticas:**
- **Sesiones Totales** → Cuántas veces has estudiado
- **Tiempo de Estudio** → Minutos acumulados
- **Precisión Global** → % de aciertos en todo
- **Racha de Días** → Días consecutivos estudiando
- **Comandos SQL** → Comandos completados en Matrix Trainer
- **Preguntas** → Preguntas respondidas en Módulos
- **Racha Actual** → Comandos sin errores seguidos
- **Mejor Racha** → Récord de comandos perfectos

**Logros:**
Los logros se desbloquean automáticamente al:
- Completar comandos/preguntas
- Alcanzar rachas
- Lograr precisión alta
- Acumular tiempo de estudio

---

## 🏆 Cómo Desbloquear Logros

| Logro | Cómo Desbloquearlo |
|-------|-------------------|
| 🎯 Primer Comando | Completa 1 comando en Matrix Trainer |
| ⚡ Maestro SQL I | Completa 10 comandos |
| 🏆 Maestro SQL II | Completa 50 comandos |
| 🔥 Racha Perfecta | 5 comandos sin errores seguidos |
| ⚡ Velocista | Completa un comando en <30 segundos |
| 📚 Primera Respuesta | Responde 1 pregunta en Módulos |
| 🎓 Buscador de Conocimiento | Responde 100 preguntas |
| 🎯 Precisión Maestra | 90% de aciertos con 20+ preguntas |
| ⏰ Estudiante Dedicado | Acumula 1 hora de estudio |
| 🏃 Maratonista | Acumula 10 horas de estudio |
| 📅 Aprendiz Constante | 7 días de racha consecutiva |

---

## 💡 Consejos de Estudio

### Para Principiantes
1. Empieza con **Matrix Trainer Classic**
2. Luego pasa a **Matrix Trainer v2 en modo guiado**
3. Finalmente usa **Estudio de Módulos**
4. Estudia 30 minutos diarios para mantener racha

### Para Nivel Intermedio
1. Usa **Matrix Trainer v2 en modo libre**
2. Practica **Estudio de Módulos** en secciones específicas
3. Revisa estadísticas para identificar debilidades
4. Apunta a 80%+ de precisión

### Para Avanzados
1. **Modo libre** en todo
2. Intenta hacer comandos en <30 segundos
3. Mantén rachas largas sin errores
4. Repasa solo preguntas "Nuevas" y "Practicar"

---

## 🔍 Solución Rápida de Problemas

**"No abre la aplicación"**
→ Verifica que PyQt5 esté instalado: `pip install PyQt5`

**"Las estadísticas no se guardan"**
→ Cierra la app con ESC, no forzando el cierre

**"El autocompletado no funciona"**
→ Presiona Ctrl+Space explícitamente

**"No veo mis logros"**
→ Necesitas completar al menos una acción

---

## 📁 Archivos Importantes

**NO ELIMINAR:**
- `user_stats.json` → Tus estadísticas y progreso
- `dp700_*.csv` → Preguntas de los módulos
- `command_*.xml` → Comandos SQL para practicar

**Puedes eliminar:**
- `__pycache__/` → Cache de Python (se regenera)

---

## 🎯 Plan de Estudio Sugerido

### Semana 1-2: Fundamentos
- Matrix Trainer Classic: 15 min/día
- Estudio de Módulos (sección básica): 15 min/día
- **Meta**: Desbloquear logros básicos

### Semana 3-4: Práctica Intensiva
- Matrix Trainer v2 (modo guiado): 20 min/día
- Estudio de Módulos (todas secciones): 20 min/día
- **Meta**: 70%+ precisión, racha de 7 días

### Semana 5-6: Simulación de Examen
- Matrix Trainer v2 (modo libre): 15 min/día
- Estudio de Módulos (práctica focalizada): 30 min/día
- **Meta**: 90%+ precisión, comandos rápidos

### Semana antes del examen
- Repaso de preguntas "Practicar"
- Comandos en modo libre rápido
- **Meta**: Confianza total

---

## 🌟 Funciones Ocultas

1. **Click en estadísticas de dominio** → Ver preguntas filtradas
2. **ESC en cualquier ventana** → Cierre rápido
3. **Modo guiado/libre** → Toggle en tiempo real
4. **Tabs en info panel** → Objetivo, Pistas, Solución

---

**¡Buena suerte en tu certificación DP-700!** 🚀

*Para más detalles, consulta README.md*
