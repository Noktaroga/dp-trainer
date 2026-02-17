import csv
import os
import random

def load_questions(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append(row)
    return questions

def get_sections(questions):
    sections = set()
    for q in questions:
        sections.add(q['section'])
    return sorted(sections)

def select_section(sections):
    print("\n=== Seleccionar Sección ===")
    for i, sec in enumerate(sections, 1):
        print(f"{i}. {sec}")
    print("0. Salir")
    while True:
        try:
            choice = int(input("Elige sección (número): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(sections):
                return sections[choice - 1]
            else:
                print(f"Elige entre 1 y {len(sections)}.")
        except ValueError:
            print("Ingresa un número.")

def select_mode():
    print("\n=== Seleccionar Modo ===")
    print("1. Modo de estudio normal")
    print("2. Modo de refuerzo")
    print("3. Modo con verificación")
    print("0. Volver al menú de secciones")
    while True:
        try:
            choice = int(input("Elige modo (1-3, 0 para volver): "))
            if choice in [0, 1, 2, 3]:
                return choice
            else:
                print("Elige 1, 2, 3 o 0.")
        except ValueError:
            print("Ingresa un número.")

def select_submode():
    print("\n=== Modo de Refuerzo ===")
    print("1. Repasar conceptos dominados")
    print("2. Repasar conceptos no dominados")
    print("0. Volver")
    while True:
        try:
            choice = int(input("Elige submodo (1-2, 0 para volver): "))
            if choice in [0, 1, 2]:
                return choice
            else:
                print("Elige 1, 2 o 0.")
        except ValueError:
            print("Ingresa un número.")

def ask_verification_mode():
    while True:
        verification = input("¿Quieres hacer la pregunta de verificación para confirmar tu comprensión? (S/N): ").strip().lower()
        if verification == 's':
            return True
        elif verification == 'n':
            return False
        else:
            print("Opción no válida. Responde 'S' o 'N'.")

def filter_questions(questions, section, mode, submode):
    filtered = [q for q in questions if q['section'] == section]
    if mode == 2:
        if submode == 1:  # dominados
            filtered = [q for q in filtered if q['metrics'] and int(q['metrics'].split(';')[0]) > 3]
        elif submode == 2:  # no dominados
            filtered = [q for q in filtered if q['metrics'] and int(q['metrics'].split(';')[0]) <= 3]
    return filtered

def show_question(question):
    print(f"\nPregunta {question['id']}: \033[32m{question['question']}\033[0m")
    options = question['options'].split(';')
    for i, opt in enumerate(options, 1):
        print(f"{i}) \033[33m{opt}\033[0m")

def get_answer(options_count):
    while True:
        try:
            answer = int(input("Tu respuesta (número): "))
            if 1 <= answer <= options_count:
                return answer
            else:
                print(f"Elige un número entre 1 y {options_count}.")
        except ValueError:
            print("Ingresa un número válido.")

def check_answer(question, answer):
    correct = int(question['correct'])
    return answer == correct

def show_feedback(question, is_correct):
    if is_correct:
        print("✔ Correcto")
    else:
        print("✗ Incorrecto")
    print(f"\033[90mNotas: {question['notas']}\033[0m")

def show_second_question(question):
    print(f"\nPregunta de verificación: \033[32m{question['second_question']}\033[0m")
    options = question['second_options'].split(';')
    for i, opt in enumerate(options, 1):
        print(f"{i}) \033[33m{opt}\033[0m")
    answer = get_answer(len(options))
    correct = int(question['second_correct'])
    if answer == correct:
        print("✔ Verificación correcta")
    else:
        print("✗ Verificación incorrecta")
    print(f"\033[90mExplicación: {question['second_explanation']}\033[0m")

def main():
    file_path = 'dp700_implement_a_lakehouse_with_microsoft_fabric_fixed.csv'
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado.")
        return

    questions = load_questions(file_path)
    sections = get_sections(questions)

    while True:
        section = select_section(sections)
        if section is None:
            break

        mode = select_mode()
        if mode == 0:
            continue

        submode = None
        if mode == 2:
            submode = select_submode()
            if submode == 0:
                continue

        verification_mode = False
        if mode == 3:
            verification_mode = True
        else:
            verification_mode = ask_verification_mode()

        filtered_questions = filter_questions(questions, section, mode, submode)
        if not filtered_questions:
            print("No hay preguntas que coincidan con los criterios seleccionados.")
            continue

        random.shuffle(filtered_questions)
        for question in filtered_questions:
            show_question(question)
            options_count = len(question['options'].split(';'))
            answer = get_answer(options_count)
            is_correct = check_answer(question, answer)
            show_feedback(question, is_correct)
            if verification_mode and question['second_question']:
                show_second_question(question)
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()