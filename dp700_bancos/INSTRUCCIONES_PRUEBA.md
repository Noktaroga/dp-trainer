# 🧪 INSTRUCCIONES DE PRUEBA

## ¡Tu sistema de entrenamiento DP-700 v2.0 está listo! 🚀

---

## 📦 Archivos Creados

### ✨ Nuevos Módulos (8 archivos)
```
stats_manager.py          (13 KB)  - Sistema de estadísticas
sql_syntax_highlighter.py (6.0 KB) - Syntax highlighting SQL
matrix_trainer_v2.py      (25 KB)  - Consola SQL real
menu_principal_v2.py      (19 KB)  - Dashboard mejorado
launch.py                 (3.0 KB) - Lanzador interactivo
start.sh                  (374 B)  - Script de inicio rápido
```

### 📚 Documentación (4 archivos)
```
README.md             (6.2 KB) - Documentación completa
GUIA_RAPIDA.md        (5.6 KB) - Guía de inicio rápido
CHANGELOG.md          (4.6 KB) - Historia de versiones
RESUMEN_MEJORAS.md    (8.5 KB) - Resumen ejecutivo
```

### 🔧 Archivos Mejorados
```
estudio_modulos.py    (49 KB)  - Integrado con stats_manager
```

---

## 🚀 Cómo Probar el Sistema

### Opción 1: Script de Inicio (Más Rápido)
```bash
cd /home/durottar/Documents/Fabric/dp700_bancos
./start.sh
```

### Opción 2: Lanzador Interactivo
```bash
cd /home/durottar/Documents/Fabric/dp700_bancos
python3 launch.py
```

### Opción 3: Directo al Dashboard
```bash
cd /home/durottar/Documents/Fabric/dp700_bancos
python3 menu_principal_v2.py
```

---

## 🎯 Qué Probar

### 1️⃣ Dashboard Principal (1-2 minutos)

**Qué verás:**
- ✅ Header con ASCII art DP-700
- ✅ 8 tarjetas estadísticas (todas en 0 al inicio)
- ✅ 3 botones de modos de entrenamiento
- ✅ Sección de logros (vacía al inicio)

**Qué hacer:**
1. Observa el diseño premium Matrix
2. Pasa el mouse sobre las tarjetas (efecto hover)
3. Lee los botones de entrenamiento

---

### 2️⃣ Matrix Trainer v2 - ⚡ NUEVO (5-10 minutos)

**Cómo acceder:**
Desde el dashboard → Click en "MATRIX TRAINER v2.0 - CONSOLA SQL REAL"

**Qué probar:**

#### a) Syntax Highlighting
1. El comando aparecerá en el panel superior
2. En el editor SQL inferior, empieza a escribir: `CREATE TABLE`
3. ✅ Verás las palabras en VERDE (keywords SQL)

#### b) Autocompletado
1. Escribe: `SEL` (solo eso)
2. Presiona `Ctrl+Space`
3. ✅ Aparecerá un menú con "SELECT"
4. Selecciona y presiona Enter

#### c) Validación Completa
1. Escribe el comando completo (copia del panel superior)
2. Presiona `F5` o `Ctrl+Enter`
3. ✅ Si es correcto: Mensaje verde "CORRECTO"
4. ✅ Si es incorrecto: Pistas específicas en amarillo

#### d) Modo Guiado vs Libre
1. Click en botón "Modo: GUIADO"
2. Cambiará a "Modo: LIBRE"
3. ✅ En libre: Sin pistas detalladas
4. ✅ En guiado: Pistas palabra por palabra

#### e) Historial de Comandos
1. Escribe un comando y presiona F5
2. Escribe otro comando diferente
3. Presiona `Ctrl+↑` (flecha arriba)
4. ✅ Verás el comando anterior

**Comandos disponibles para probar:**
- command_01_drop_table.xml
- command_02_create_table.xml
- command_03_select_trip.xml
- command_04_metadata_trip.xml
- command_05_insert_staging.xml
- command_06_row_number.xml
- command_07_createdat.xml

---

### 3️⃣ Estudio de Módulos (5-10 minutos)

**Cómo acceder:**
Desde el dashboard → Click en "MODO ESTUDIO DE MÓDULOS"

**Qué probar:**

#### a) Panel de Dominio
1. Selecciona un módulo del dropdown
2. ✅ Verás el panel de estadísticas de dominio:
   - Total de preguntas
   - Dominadas (≥80%)
   - Para practicar (40-79%)
   - Nuevas (<40%)
3. Click en cada categoría para ver detalles

#### b) Estudiar Preguntas
1. Click en "INICIAR ESTUDIO"
2. Responde algunas preguntas
3. ✅ Verás feedback inmediato (verde/rojo)
4. ✅ Notas explicativas
5. ✅ Progreso actualizado

#### c) Estadísticas Globales
1. Responde al menos 5 preguntas
2. Cierra el estudio
3. Vuelve al dashboard
4. ✅ Verás actualizadas:
   - Preguntas respondidas
   - Precisión global
   - Tiempo de estudio

---

### 4️⃣ Sistema de Logros (2-3 minutos)

**Cómo desbloquear:**

1. **🎯 Primer Comando**
   - Completa 1 comando en Matrix Trainer v2
   
2. **📚 Primera Respuesta**
   - Responde 1 pregunta en Estudio de Módulos

3. **⏰ Estudiante Dedicado**
   - Estudia durante varios minutos

**Verificar:**
1. Vuelve al dashboard
2. ✅ Verás badges en "LOGROS RECIENTES"

---

### 5️⃣ Estadísticas Persistentes (1 minuto)

**Verificar:**
1. Usa el sistema durante 5-10 minutos
2. Cierra TODO (dashboard y apps)
3. Verifica que existe: `user_stats.json`
4. Abre de nuevo el dashboard
5. ✅ Las estadísticas se mantienen

---

## 🎨 Características Visuales a Observar

### Estética Matrix Premium
- ✅ Verde (#00FF00) sobre negro (#000000)
- ✅ Tipografía Courier New monospace
- ✅ Bordes redondeados con border-radius
- ✅ Efectos hover (pasa el mouse sobre elementos)

### Animaciones
- ✅ Fade-in al abrir dashboard
- ✅ Hover effects en tarjetas
- ✅ Transiciones suaves en botones
- ✅ Barras de progreso con gradientes

### Feedback Visual
- ✅ Verde = Correcto/Positivo
- ✅ Amarillo = Advertencia/Pistas
- ✅ Rojo = Error/Incorrecto
- ✅ Cyan = Información

---

## 🧪 Tests Específicos

### Test 1: Comando Completo en Consola SQL
```
1. Abre Matrix Trainer v2
2. Copia este comando:
   CREATE TABLE dbo.Test (ID INT, Name VARCHAR(50));
3. Pégalo en el editor
4. Presiona F5
5. ✅ Debería validarse correctamente
```

### Test 2: Autocompletado
```
1. Escribe solo: "SEL"
2. Ctrl+Space
3. Enter en SELECT
4. Espacio
5. Escribe: "COU"
6. Ctrl+Space
7. ✅ Debería aparecer COUNT
```

### Test 3: Racha de Comandos
```
1. Completa 3 comandos seguidos sin errores
2. Ve al dashboard
3. ✅ "Racha Actual" debería mostrar "3"
4. Si fallas uno
5. ✅ "Racha Actual" vuelve a "0"
```

### Test 4: Precisión en Módulos
```
1. Responde 10 preguntas en Estudio de Módulos
2. Intenta acertar al menos 8
3. Ve al dashboard
4. ✅ "Precisión Global" debería ser ≥80%
```

---

## 📊 Archivos Generados Automáticamente

Después de usar el sistema, verás:

```
user_stats.json  - Todas tus estadísticas
__pycache__/     - Cache de Python (normal)
```

**NO elimines `user_stats.json`** - contiene todo tu progreso.

---

## 🐛 Si Algo No Funciona

### Error: "ModuleNotFoundError: No module named 'PyQt5'"
```bash
pip install PyQt5
```

### Error: "Permission denied" al ejecutar start.sh
```bash
chmod +x start.sh
```

### No se guardan las estadísticas
- Cierra las apps con ESC, no forzando
- Verifica permisos de escritura en el directorio

### El syntax highlighting no funciona
- Verifica que sql_syntax_highlighter.py está presente
- Reinicia la aplicación

---

## ✅ Checklist de Verificación

- [ ] Dashboard abre correctamente
- [ ] Matrix Trainer v2 abre y muestra comandos
- [ ] Syntax highlighting funciona (palabras en verde)
- [ ] Autocompletado funciona (Ctrl+Space)
- [ ] Validación de comandos funciona (F5)
- [ ] Estudio de Módulos abre y muestra preguntas
- [ ] Estadísticas se actualizan en dashboard
- [ ] Logros se desbloquean
- [ ] user_stats.json se crea
- [ ] Las estadísticas persisten después de cerrar

---

## 📖 Documentación Disponible

Si necesitas más información:

1. **README.md** → Documentación completa
2. **GUIA_RAPIDA.md** → Inicio rápido y tips
3. **CHANGELOG.md** → Historial de versiones
4. **RESUMEN_MEJORAS.md** → Lista de mejoras implementadas

---

## 🎓 Siguiente Paso

Una vez que hayas probado todo:

1. Lee el **GUIA_RAPIDA.md** para tips de estudio
2. Sigue el plan de estudio sugerido
3. Mantén una racha de 7 días para el logro "Aprendiz Constante"
4. Apunta a 90%+ de precisión
5. Practica comandos en <30 segundos

---

## 🏆 Meta Inicial

**Objetivo para la primera semana:**
- [ ] Desbloquear "Primer Comando"
- [ ] Desbloquear "Primera Respuesta"
- [ ] Alcanzar 70%+ de precisión
- [ ] Estudiar al menos 30 minutos
- [ ] Completar 5 comandos
- [ ] Responder 20 preguntas

---

**¡El sistema está listo para usarse!** 🎉

**Comando rápido para empezar:**
```bash
cd /home/durottar/Documents/Fabric/dp700_bancos && ./start.sh
```

O simplemente:
```bash
cd ~/Documents/Fabric/dp700_bancos && python3 menu_principal_v2.py
```

**¡Buena suerte con tu certificación DP-700!** 🚀
