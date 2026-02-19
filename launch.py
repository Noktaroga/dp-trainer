#!/usr/bin/env python3
"""
Script de lanzamiento rápido para DP-700 Training System
"""

import sys
import subprocess
import os

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import PyQt5
        return True
    except ImportError:
        print("❌ ERROR: PyQt5 no está instalado")
        print("\n📦 Para instalar, ejecuta:")
        print("   pip install PyQt5")
        return False

def main():
    """Menú de lanzamiento rápido"""
    if not check_dependencies():
        sys.exit(1)
    
    print("=" * 60)
    print("  DP-700 TRAINING SYSTEM v2.0 - Matrix Edition")
    print("  Microsoft Fabric Data Engineer")
    print("=" * 60)
    print()
    print("Selecciona una opción:")
    print()
    print("  1. 🎯 Dashboard Principal (Recomendado)")
    print("  2. ⚡ Matrix Trainer v2 - Consola SQL Real (NUEVO)")
    print("  3. 📝 Matrix Trainer Classic")
    print("  4. 📚 Estudio de Módulos")
    print("  5. ℹ️  Ver README")
    print("  0. ❌ Salir")
    print()
    
    while True:
        try:
            choice = input("Opción: ").strip()
            
            if choice == "0":
                print("\n👋 ¡Hasta luego!")
                sys.exit(0)
            
            elif choice == "1":
                print("\n🚀 Lanzando Dashboard Principal...")
                subprocess.run([sys.executable, "menu_principal_v2.py"])
                break
            
            elif choice == "2":
                print("\n⚡ Lanzando Matrix Trainer v2...")
                subprocess.run([sys.executable, "matrix_trainer_v2.py"])
                break
            
            elif choice == "3":
                print("\n📝 Lanzando Matrix Trainer Classic...")
                subprocess.run([sys.executable, "matrix_trainer.py"])
                break
            
            elif choice == "4":
                print("\n📚 Lanzando Estudio de Módulos...")
                subprocess.run([sys.executable, "estudio_modulos.py"])
                break
            
            elif choice == "5":
                print("\n📄 Abriendo README...")
                if os.path.exists("README.md"):
                    with open("README.md", "r", encoding="utf-8") as f:
                        print("\n" + "=" * 60)
                        print(f.read())
                        print("=" * 60 + "\n")
                else:
                    print("❌ No se encontró el archivo README.md")
                input("\nPresiona ENTER para continuar...")
                main()  # Volver al menú
                break
            
            else:
                print("❌ Opción inválida. Intenta de nuevo.")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
