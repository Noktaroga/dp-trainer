import csv
import os
import random
import glob

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

def select_multiple_sections(sections):
    print("\n=== Seleccionar Múltiples Secciones ===")
    for i, sec in enumerate(sections, 1):
        print(f"{i}. {sec}")
    print("Ingresa los números separados por comas (ej: 1,3,5), o 0 para cancelar.")
    while True:
        try:
            choice = input("Elige secciones: ").strip()
            if choice == '0':
                return None
            indices = [int(x.strip()) for x in choice.split(',')]
            selected = []
            for idx in indices:
                if 1 <= idx <= len(sections):
                    selected.append(sections[idx - 1])
                else:
                    print(f"Número {idx} inválido.")
                    selected = []
                    break
            if selected:
                return selected
        except ValueError:
            print("Ingresa números separados por comas.")

def ask_repetitions():
    while True:
        try:
            reps = int(input("Número de repeticiones (veces que se repetirán todas las preguntas): "))
            if reps > 0:
                return reps
            else:
                print("Ingresa un número mayor a 0.")
        except ValueError:
            print("Ingresa un número válido.")

def ask_verification_mode():
    while True:
        verification = input("¿Quieres hacer la pregunta de verificación para confirmar tu comprensión? (S/N): ").strip().lower()
        if verification == 's':
            return True
        elif verification == 'n':
            return False
        else:
            print("Opción no válida. Responde 'S' o 'N'.")

def show_question(question):
    print(f"\nPregunta {question['id']}: \033[32m{question['question']}\033[0m")
    if question['multi'].lower() == 'true':
        print("(Pregunta de múltiples respuestas)")
    options = question['options'].split(';')
    for i, opt in enumerate(options, 1):
        print(f"{i}) \033[33m{opt}\033[0m")

def get_answer(options_count, is_multi=False):
    if is_multi:
        while True:
            try:
                answers = input("Tu respuesta (números separados por comas): ").strip()
                answer_list = [int(x.strip()) for x in answers.split(',')]
                if all(1 <= a <= options_count for a in answer_list):
                    return answer_list
                else:
                    print(f"Elige números entre 1 y {options_count}.")
            except ValueError:
                print("Ingresa números separados por comas.")
    else:
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
    if question['multi'].lower() == 'true':
        correct_list = [int(x) for x in question['correct'].split(';')]
        return set(answer) == set(correct_list)
    else:
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
    files = glob.glob('*.csv')
    if not files:
        print("No se encontraron archivos CSV.")
        return

    all_sections = set()
    section_to_file = {}
    for file in files:
        if not os.path.exists(file):
            continue
        questions = load_questions(file)
        sections = get_sections(questions)
        for sec in sections:
            all_sections.add(sec)
            section_to_file[sec] = file  # Asumiendo secciones únicas por archivo

    sections = sorted(all_sections)
    if not sections:
        print("No se encontraron secciones en los archivos.")
        return

    print("=== Modo de Estudio Múltiple ===")

    selected_sections = select_multiple_sections(sections)
    if not selected_sections:
        print("Cancelado.")
        return

    repetitions = ask_repetitions()

    verification_mode = ask_verification_mode()

    # Collect all questions from selected sections
    selected_questions = []
    for sec in selected_sections:
        file = section_to_file[sec]
        questions = load_questions(file)
        selected_questions.extend([q for q in questions if q['section'] == sec])

    if not selected_questions:
        print("No hay preguntas en las secciones seleccionadas.")
        return

    print(f"\nIniciando estudio con {len(selected_questions)} preguntas, repetido {repetitions} veces.")
    print("Preguntas aleatorias en cada repetición.")

    for rep in range(1, repetitions + 1):
        print(f"\n--- Repetición {rep} ---")
        shuffled_questions = selected_questions.copy()
        random.shuffle(shuffled_questions)
        for question in shuffled_questions:
            show_question(question)
            options_count = len(question['options'].split(';'))
            is_multi = question['multi'].lower() == 'true'
            answer = get_answer(options_count, is_multi)
            is_correct = check_answer(question, answer)
            show_feedback(question, is_correct)
            if verification_mode and question['second_question']:
                show_second_question(question)
            input("Presiona Enter para continuar...")

    print("\nEstudio completado.")

if __name__ == "__main__":
    main()