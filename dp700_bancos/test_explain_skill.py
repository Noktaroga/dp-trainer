#!/usr/bin/env python3
"""Test file to demonstrate explain-code skill"""

def bubble_sort(arr):
    """
    Ordena una lista usando el algoritmo Bubble Sort.
    
    Args:
        arr: Lista de elementos comparables
        
    Returns:
        Lista ordenada
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


class BankAccount:
    """Representa una cuenta bancaria simple"""
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("El monto debe ser positivo")
        self.balance += amount
        self.transactions.append(f"Depósito: +${amount}")
        return self.balance
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Fondos insuficientes")
        self.balance -= amount
        self.transactions.append(f"Retiro: -${amount}")
        return self.balance


# Ejemplo de uso
if __name__ == "__main__":
    # Test bubble sort
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {numbers}")
    print(f"Ordenado: {bubble_sort(numbers.copy())}")
    
    # Test bank account
    account = BankAccount("Juan", 100)
    account.deposit(50)
    account.withdraw(30)
    print(f"\nCuenta de {account.owner}: ${account.balance}")
    print(f"Transacciones: {account.transactions}")
