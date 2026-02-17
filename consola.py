import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import random

BANK_DIR = Path("dp700_bancos")  # Carpeta con los CSV generados

# -------------------------------
# Utilidades de carga y guardado
# -------------------------------

def cargar_preguntas_desde_bancos(bank_dir: Path):
    """
    Lee todos los CSV de la carpeta bank_dir y devuelve:
      - lista de preguntas
      - mapa archivo -> lista de filas originales para poder actualizar notas
    Cada CSV debe tener cabecera:
      section,id,question,options,correct,multi,notas,metrics
    """
    preguntas = []
    archivos_data = {}  # {Path: [dict_row]}

    if not bank_dir.exists():
        print(f"La carpeta {bank_dir} no existe. Ejecuta primero el generador de bancos.")
        return preguntas, archivos_data

    for csv_file in bank_dir.glob("*.csv"):
        with open(csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                rows.append(row)

                section = row["section"].strip()
                id_str = row.get("id", "").strip()
                if not id_str or not id_str.isdigit():
                    continue  # skip invalid rows silently
                qid = int(id_str)
                question = row["question"].strip()
                options = [opt.strip() for opt in row["options"].split(";")]
                correct_str = row["correct"].strip()
                if correct_str:
                    correct_indices = []
                    for x in correct_str.split(";"):
                        x = x.strip()
                        if x.isdigit():
                            correct_indices.append(int(x) - 1)
                        else:
                            print(f"Warning: non-numeric correct value '{x}' in question {qid}, skipping")
                else:
                    correct_indices = []
                multi = row["multi"].strip().lower() == "true"
                notas = (row.get("notas") or "").strip()
                metrics_str = (row.get("metrics") or "0;0").strip()
                try:
                    correct_count, incorrect_count = map(int, metrics_str.split(";"))
                except ValueError:
                    print(f"Warning: invalid metrics '{metrics_str}' in question {qid}, setting to 0;0")
                    correct_count, incorrect_count = 0, 0
                second_question = (row.get("second_question") or "").strip()
                second_options = [opt.strip() for opt in (row.get("second_options") or "").split(";")]
                second_correct_str = (row.get("second_correct") or "").strip()
                if second_correct_str and second_correct_str.isdigit():
                    second_correct = int(second_correct_str) - 1
                else:
                    second_correct = None
                second_explanation = (row.get("second_explanation") or "").strip()

                preguntas.append({
                    "section": section,
                    "id": qid,
                    "question": question,
                    "options": options,
                    "correct": sorted(correct_indices),
                    "multi": multi,
                    "notas": notas,
                    "metrics": {"correct": correct_count, "incorrect": incorrect_count},
                    "second_question": second_question,
                    "second_options": second_options,
                    "second_correct": second_correct,
                    "second_explanation": second_explanation,
                    "source_file": csv_file,   # para saber qué archivo actualizar
                })
            archivos_data[csv_file] = rows

    return preguntas, archivos_data

def agrupar_por_seccion(preguntas):
    secciones = defaultdict(list)
    for q in preguntas:
        secciones[q["section"]].append(q)
    return secciones

def actualizar_notas_en_archivo(archivos_data, pregunta, nueva_nota):
    """
    Actualiza la columna 'notas' para la pregunta dada (por section + id)
    en el CSV de origen, agregando la nueva nota separada por '|'.
    """
    csv_path = pregunta["source_file"]
    if csv_path not in archivos_data:
        return

    rows = archivos_data[csv_path]
    target_section = pregunta["section"]
    target_id = str(pregunta["id"])

    for row in rows:
        if row["section"].strip() == target_section and row["id"].strip() == target_id:
            notas_actuales = row.get("notas", "").strip()
            if notas_actuales:
                row["notas"] = notas_actuales + "|" + nueva_nota
            else:
                row["notas"] = nueva_nota
            # actualizar también en la instancia en memoria
            pregunta["notas"] = row["notas"]
            break

    # reescribir el archivo completo con las notas actualizadas
    fieldnames = ["section", "id", "question", "options", "correct", "multi", "notas", "metrics", "second_question", "second_options", "second_correct", "second_explanation"]
    with open(csv_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            # asegurar que 'notas' existe
            if "notas" not in row:
                row["notas"] = ""
            if "metrics" not in row:
                row["metrics"] = "0;0"
            if "second_question" not in row:
                row["second_question"] = ""
            if "second_options" not in row:
                row["second_options"] = ""
            if "second_correct" not in row:
                row["second_correct"] = ""
            if "second_explanation" not in row:
                row["second_explanation"] = ""
            writer.writerow({
                "section": row["section"],
                "id": row["id"],
                "question": row["question"],
                "options": row["options"],
                "correct": row["correct"],
                "multi": row["multi"],
                "notas": row.get("notas", ""),
                "metrics": row.get("metrics", "0;0"),
                "second_question": row.get("second_question", ""),
                "second_options": row.get("second_options", ""),
                "second_correct": row.get("second_correct", ""),
                "second_explanation": row.get("second_explanation", ""),
            })

def actualizar_metricas_en_archivo(archivos_data, pregunta, is_correct):
    """
    Actualiza las métricas para la pregunta dada.
    """
    csv_path = pregunta["source_file"]
    if csv_path not in archivos_data:
        return

    rows = archivos_data[csv_path]
    target_section = pregunta["section"]
    target_id = str(pregunta["id"])

    for row in rows:
        if row["section"].strip() == target_section and row["id"].strip() == target_id:
            metrics_str = row.get("metrics", "0;0")
            try:
                correct_count, incorrect_count = map(int, metrics_str.split(";"))
            except ValueError:
                correct_count, incorrect_count = 0, 0
            if is_correct:
                correct_count += 1
            else:
                incorrect_count += 1
            row["metrics"] = f"{correct_count};{incorrect_count}"
            # actualizar en memoria
            pregunta["metrics"]["correct"] = correct_count
            pregunta["metrics"]["incorrect"] = incorrect_count
            break

    # reescribir el archivo
    fieldnames = ["section", "id", "question", "options", "correct", "multi", "notas", "metrics", "second_question", "second_options", "second_correct", "second_explanation"]
    with open(csv_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if "notas" not in row:
                row["notas"] = ""
            if "metrics" not in row:
                row["metrics"] = "0;0"
            if "second_question" not in row:
                row["second_question"] = ""
            if "second_options" not in row:
                row["second_options"] = ""
            if "second_correct" not in row:
                row["second_correct"] = ""
            if "second_explanation" not in row:
                row["second_explanation"] = ""
            writer.writerow({
                "section": row["section"],
                "id": row["id"],
                "question": row["question"],
                "options": row["options"],
                "correct": row["correct"],
                "multi": row["multi"],
                "notas": row.get("notas", ""),
                "metrics": row.get("metrics", "0;0"),
                "second_question": row.get("second_question", ""),
                "second_options": row.get("second_options", ""),
                "second_correct": row.get("second_correct", ""),
                "second_explanation": row.get("second_explanation", ""),
            })

# -------------------------------
# Interfaz de consola
# -------------------------------

def clear_screen():
    print("\n" + "-" * 60 + "\n")

def mostrar_menu_secciones(secciones):
    clear_screen()
    print("=== DP-700 Quiz (bancos CSV) ===\n")
    keys = sorted(secciones.keys())
    for idx, sec in enumerate(keys, start=1):
        print(f"{idx}. {sec} ({len(secciones[sec])} preguntas)")
    print("R. Recargar bancos (leer de nuevo los CSV)")
    print("0. Salir\n")
    return keys

def mostrar_menu_modos():
    clear_screen()
    print("=== Seleccionar Modo ===")
    print("1. Modo de estudio normal")
    print("2. Modo de refuerzo")
    print("3. Modo con verificación")
    print("0. Volver al menú de secciones")
    print()

def elegir_opcion(keys):
    while True:
        choice = input("Elige opción: ").strip().upper()
        if choice == "R":
            return "R"
        if choice.isdigit():
            n = int(choice)
            if 0 <= n <= len(keys):
                return n
        print("Entrada inválida. Usa un número o 'R'.")

def elegir_modo():
    while True:
        choice = input("Elige modo (1-3, 0 para volver): ").strip()
        if choice in ["0", "1", "2", "3"]:
            return int(choice)
        print("Entrada inválida. Usa 0, 1, 2 o 3.")

def mostrar_menu_refuerzo():
    clear_screen()
    print("=== Modo de Refuerzo ===")
    print("1. Repasar conceptos dominados")
    print("2. Repasar conceptos no dominados")
    print("0. Volver")
    print()

def elegir_refuerzo():
    while True:
        choice = input("Elige submodo (1-2, 0 para volver): ").strip()
        if choice in ["0", "1", "2"]:
            return int(choice)
        print("Entrada inválida. Usa 0, 1 o 2.")

def calcular_dominio(q):
    correct = q["metrics"]["correct"]
    incorrect = q["metrics"]["incorrect"]
    total = correct + incorrect
    if total == 0:
        return 0.0
    return correct / total

def es_dominada(q, min_total=5):
    """
    Una pregunta es dominada si tiene al menos min_total respuestas y porcentaje >= 70%.
    """
    correct = q["metrics"]["correct"]
    incorrect = q["metrics"]["incorrect"]
    total = correct + incorrect
    if total < min_total:
        return False
    return (correct / total) >= 0.7

def seleccionar_preguntas(preguntas_seccion, minimo=5, maximo=15):
    total = len(preguntas_seccion)
    if total < minimo:
        print(f"\nLa sección tiene solo {total} preguntas (mínimo recomendado: {minimo}).")
    # Siempre barajar para mayor aleatoriedad
    random.shuffle(preguntas_seccion)
    return preguntas_seccion[:maximo]

def seleccionar_preguntas_con_filtro(preguntas_seccion, filtro_dominio, minimo=5, maximo=15):
    """
    Filtra preguntas basado en el filtro de dominio.
    filtro_dominio: 'dominado' para es_dominada, 'no_dominado' para no es_dominada, 'todos' para normal con pesos
    """
    if filtro_dominio == 'todos':
        # Para 'todos', dar menos peso a dominadas: seleccionar más no dominadas
        no_dominadas = [q for q in preguntas_seccion if not es_dominada(q)]
        dominadas = [q for q in preguntas_seccion if es_dominada(q)]
        # Ordenar no_dominadas por prioridad: primero no estudiadas (total==0), luego menos respuestas, luego menor porcentaje
        def prioridad(q):
            total = q["metrics"]["correct"] + q["metrics"]["incorrect"]
            pct = calcular_dominio(q)
            return (0 if total == 0 else 1, total, pct)  # 0 para total==0, luego menor total, menor pct
        no_dominadas.sort(key=prioridad)
        seleccionadas_no_dom = no_dominadas[:maximo]
        random.shuffle(seleccionadas_no_dom)  # variar orden entre priorizadas
        dominadas_selec = dominadas[:max(0, maximo - len(seleccionadas_no_dom))]
        random.shuffle(dominadas_selec)
        seleccionadas = seleccionadas_no_dom + dominadas_selec
        random.shuffle(seleccionadas)  # barajar final
        return seleccionadas[:maximo]
    
    filtradas = []
    for q in preguntas_seccion:
        if filtro_dominio == 'dominado' and es_dominada(q):
            filtradas.append(q)
        elif filtro_dominio == 'no_dominado' and not es_dominada(q):
            filtradas.append(q)
    
    if not filtradas:
        print(f"No hay preguntas que cumplan el filtro '{filtro_dominio}'. Seleccionando todas.")
        return seleccionar_preguntas(preguntas_seccion, minimo, maximo)
    
    # Para no_dominado, ordenar por prioridad y seleccionar con variación
    if filtro_dominio == 'no_dominado':
        def prioridad(q):
            total = q["metrics"]["correct"] + q["metrics"]["incorrect"]
            pct = calcular_dominio(q)
            return (0 if total == 0 else 1, total, pct)
        filtradas.sort(key=prioridad)
        seleccionadas = filtradas[:maximo]
        random.shuffle(seleccionadas)  # variar el orden entre las priorizadas
        return seleccionadas

def pedir_respuesta_o_nota(q, archivos_data):
    """
    Muestra la pregunta y permite:
      - introducir respuesta (números / enter)
      - pulsar 'N' para agregar nota antes de responder
    Devuelve la lista de índices elegidos para la respuesta.
    """
    while True:
        print(f"\nPregunta {q['id']}: {q['question']}\n")
        total_respondida = q["metrics"]["correct"] + q["metrics"]["incorrect"]
        correctas = q["metrics"]["correct"]
        print(f"Respondida {total_respondida} veces, {correctas} correctas.\n")
        # Barajar las opciones para variar el orden
        shuffled_indices = list(range(len(q["options"])))
        random.shuffle(shuffled_indices)
        for idx, old_i in enumerate(shuffled_indices, start=1):
            print(f"  {idx}) {q['options'][old_i]}")

        if q["notas"]:
            print(f"\nNotas actuales: {q['notas']}")

        if q["multi"]:
            print("\n(Puede haber varias correctas. Separa con comas, ej: 1,3,4)")
        else:
            print("\n(Selecciona una sola opción)")

        print("Pulsa 'N' para agregar nota a esta pregunta.")

        ans = input("Tu respuesta (o N para nota): ").strip()

        # Manejo de notas
        if ans.upper() == "N":
            if q["notas"]:
                print("\nNotas actuales:")
                for nota in q["notas"].split("|"):
                    print(f"- {nota}")
            else:
                print("\nNo hay notas actuales.")
            nota = input("\nEscribe tu nueva nota (o Enter para cancelar): ").strip()
            if nota:
                actualizar_notas_en_archivo(archivos_data, q, nota)
                print("Nota guardada.\n")
            # luego vuelve a mostrar la pregunta para responderla
            continue

        if not ans:
            print("La respuesta no puede estar vacía.")
            continue

        parts = [p.strip() for p in ans.replace(";", ",").split(",")]
        if all(p.isdigit() for p in parts):
            user_nums = [int(p) for p in parts]
            if all(1 <= i <= len(q["options"]) for i in user_nums):
                user_old_indices = sorted([shuffled_indices[i-1] for i in user_nums])
                return user_old_indices

        print("Entrada inválida. Usa números de opciones (ej: 2 o 1,3) o 'N' para nota.")

def evaluar(q, user_idx):
    return user_idx == q["correct"]

def puntuacion(num_ok, total):
    if total == 0:
        return 0.0
    return round(100.0 * num_ok / total, 2)

# -------------------------------
# Bucle principal
# -------------------------------

def run():
    preguntas, archivos_data = cargar_preguntas_desde_bancos(BANK_DIR)
    if not preguntas:
        print("No se pudieron cargar preguntas. Revisa la carpeta dp700_bancos.")
        return

    secciones = agrupar_por_seccion(preguntas)

    while True:
        keys = mostrar_menu_secciones(secciones)
        choice = elegir_opcion(keys)

        if choice == "R":
            preguntas, archivos_data = cargar_preguntas_desde_bancos(BANK_DIR)
            secciones = agrupar_por_seccion(preguntas)
            print("\nBancos recargados desde los CSV.")
            input("Enter para continuar...")
            continue

        if choice == 0:
            print("Saliendo. ¡Buen estudio para el DP-700!")
            break

        section_name = keys[choice - 1]
        clear_screen()
        print(f"=== Sección: {section_name} ===")

        # Seleccionar modo
        while True:
            mostrar_menu_modos()
            modo = elegir_modo()
            if modo == 0:
                break  # volver al menú de secciones
            elif modo == 1:
                filtro = 'todos'
                modo_str = "Modo Normal"
            elif modo == 2:
                mostrar_menu_refuerzo()
                submodo = elegir_refuerzo()
                if submodo == 0:
                    continue
                elif submodo == 1:
                    filtro = 'dominado'
                    modo_str = "Refuerzo - Conceptos Dominados"
                elif submodo == 2:
                    filtro = 'no_dominado'
                    modo_str = "Refuerzo - Conceptos No Dominados"
            elif modo == 3:
                filtro = 'todos'
                modo_str = "Modo con Verificación"
            
            clear_screen()
            print(f"=== {modo_str} ===")
            
            verification_mode = (modo == 3)
            if not verification_mode:
                verif = input("¿Quieres hacer la pregunta de verificación para confirmar tu comprensión? (S/N): ").strip().upper()
                if verif == "S":
                    verification_mode = True
            
            # Bucle de sesiones de 3 preguntas
            while True:
                preguntas_sesion = seleccionar_preguntas_con_filtro(secciones[section_name], filtro, minimo=3, maximo=3)
                if not preguntas_sesion:
                    print("No hay más preguntas para esta configuración.")
                    break

                respuestas_log = []
                correctas = 0

                for q in preguntas_sesion:
                    user_idx = pedir_respuesta_o_nota(q, archivos_data)
                    ok = evaluar(q, user_idx)
                    actualizar_metricas_en_archivo(archivos_data, q, ok)
                    if ok:
                        print("✔ Correcto\n")
                        correctas += 1
                        if verification_mode:
                            # Pregunta de verificación: elegir una no dominada si la principal es dominada
                            if es_dominada(q):
                                # Elegir una pregunta no dominada para verificación
                                no_dominadas = [pq for pq in secciones[section_name] if not es_dominada(pq) and pq != q]
                                if no_dominadas:
                                    verif_q = random.choice(no_dominadas)
                                    print(f"\nPregunta de verificación: {verif_q['question']}\n")
                                    for idx, opt in enumerate(verif_q["options"], start=1):
                                        print(f"  {idx}) {opt}")
                                    print("\n(Selecciona una sola opción)")
                                    ans = input("Tu respuesta: ").strip()
                                    if ans.isdigit():
                                        user_choice = int(ans) - 1
                                        if 0 <= user_choice < len(verif_q["options"]):
                                            if user_choice in verif_q["correct"]:
                                                print("✔ ¡Excelente! Tu comprensión es sólida.\n")
                                            else:
                                                print("✘ Respuesta incorrecta.\n")
                                                # No hay explicación predefinida, quizás agregar nota
                                        else:
                                            print("Opción inválida.\n")
                                    else:
                                        print("Entrada inválida.\n")
                                else:
                                    print("No hay preguntas no dominadas disponibles para verificación.\n")
                            else:
                                # Si no es dominada, usar la second_question si existe
                                if q["second_question"] and q["second_options"] and len(q["second_options"]) >= 2 and q["second_correct"] is not None:
                                    print(f"\nPregunta de verificación: {q['second_question']}\n")
                                    for idx, opt in enumerate(q["second_options"], start=1):
                                        print(f"  {idx}) {opt}")
                                    print("\n(Selecciona una sola opción)")
                                    ans = input("Tu respuesta: ").strip()
                                    if ans.isdigit():
                                        user_choice = int(ans) - 1
                                        if 0 <= user_choice < len(q["second_options"]):
                                            if user_choice == q["second_correct"]:
                                                print("✔ ¡Excelente! Tu comprensión es sólida.\n")
                                            else:
                                                print("✘ Respuesta incorrecta.\n")
                                                if q["second_explanation"]:
                                                    print(f"Explicación: {q['second_explanation']}\n")
                                        else:
                                            print("Opción inválida.\n")
                                    else:
                                        print("Entrada inválida.\n")
                    else:
                        print("✘ Incorrecto\n")
                        add_note = input("¿Quieres agregar una nota? (S/N): ").strip().upper()
                        if add_note == "S":
                            nota = input("Escribe tu nota: ").strip()
                            if nota:
                                actualizar_notas_en_archivo(archivos_data, q, nota)
                                print("Nota guardada.")

                    respuestas_log.append({
                        "question_id": q["id"],
                        "is_correct": ok,
                        "user_answer_indices": user_idx,
                        "correct_indices": q["correct"],
                    })

                score = puntuacion(correctas, len(preguntas_sesion))
                print(f"\nPuntuación sesión: {score}/100")

                # Preguntar si continuar
                continuar = input("\n¿Quieres continuar con más preguntas en este modo? (S/N): ").strip().upper()
                if continuar != "S":
                    break
            
            input("\nEnter para volver al menú de modos...")
            break  # salir del while de modos

if __name__ == "__main__":
    run()
