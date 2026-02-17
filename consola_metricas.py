import csv
from pathlib import Path
from collections import defaultdict

BANK_DIR = Path("dp700_bancos")  # Carpeta con los CSV generados

def calcular_metricas_modulos(bank_dir: Path):
    """
    Calcula métricas de progreso para cada módulo basado en los CSV.
    Progreso de estudio: porcentaje de preguntas con notas no vacías.
    Rendimiento: porcentaje de respuestas correctas sobre total de intentos.
    """
    metricas = {}

    if not bank_dir.exists():
        print(f"La carpeta {bank_dir} no existe.")
        return metricas

    for csv_file in bank_dir.glob("*.csv"):
        modulo = csv_file.stem  # Nombre del módulo sin extensión
        total_preguntas = 0
        preguntas_estudiadas = 0  # Con notas no vacías
        total_intentos = 0
        total_correctas = 0

        with open(csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_preguntas += 1
                metrics_str = (row.get("metrics") or "0;0").strip()
                try:
                    correct_count, incorrect_count = map(int, metrics_str.split(";"))
                    total_intentos += correct_count + incorrect_count
                    total_correctas += correct_count
                    if correct_count + incorrect_count > 0:
                        porcentaje_aciertos = correct_count / (correct_count + incorrect_count)
                        if porcentaje_aciertos > 0.8:
                            preguntas_estudiadas += 1
                except ValueError:
                    pass  # Ignorar métricas inválidas

        progreso_estudio = (preguntas_estudiadas / total_preguntas * 100) if total_preguntas > 0 else 0
        rendimiento = (total_correctas / total_intentos * 100) if total_intentos > 0 else 0

        metricas[modulo] = {
            "total_preguntas": total_preguntas,
            "preguntas_estudiadas": preguntas_estudiadas,
            "progreso_estudio": progreso_estudio,
            "total_intentos": total_intentos,
            "total_correctas": total_correctas,
            "rendimiento": rendimiento
        }

    return metricas

def mostrar_metricas(metricas):
    """
    Muestra las métricas en consola.
    """
    if not metricas:
        print("No hay métricas disponibles.")
        return

    print("=== MÉTRICAS DE PROGRESO POR MÓDULO ===\n")
    for modulo, data in metricas.items():
        print(f"Módulo: {modulo}")
        print(f"  Total de preguntas: {data['total_preguntas']}")
        print(f"  Preguntas estudiadas: {data['preguntas_estudiadas']}")
        print(f"  Progreso de estudio: {data['progreso_estudio']:.1f}%")
        print(f"  Total de intentos: {data['total_intentos']}")
        print(f"  Respuestas correctas: {data['total_correctas']}")
        print(f"  Rendimiento: {data['rendimiento']:.1f}%")
        print()

def run():
    """
    Función principal para ejecutar la consola de métricas.
    """
    print("Bienvenido a la Consola de Métricas de Estudio DP-700")
    print("Calculando métricas...\n")

    metricas = calcular_metricas_modulos(BANK_DIR)
    mostrar_metricas(metricas)

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    run()