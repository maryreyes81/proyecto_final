"""
main.py
-------
Punto de entrada en consola para el proyecto Happy Burger.

Avance 1:
- Muestra un menú con opciones:
  a) Pedidos
  b) Clientes
  c) Menú
  d) Salir
- Controla el flujo con condicionales.
- En la opción Pedidos, calcula el costo de un solo producto y
  simula el uso en pantalla.

Avances siguientes pueden reutilizar estas estructuras.
"""

from db.database import BaseDatos
from models.pedido import Pedido
from models.clientes import Clientes
from models.menu import Menu


def mostrar_menu():
    """
    Imprime en pantalla el menú principal con las opciones pedidas.
    """
    print("\n==============================")
    print("       HAPPY BURGER - APP     ")
    print("==============================")
    print("a) Pedidos")
    print("b) Clientes")
    print("c) Menú")
    print("d) Salir")
    print("==============================")


def calcular_pedido_simple():
    """
    Opción Pedidos (Avance 1).

    Solicita al usuario:
    - nombre del producto
    - precio
    - unidades

    Calcula el costo total e imprime la simulación en pantalla.
    """
    print("\n--- Opción: Pedidos (cálculo simple) ---")

    nombre_producto = input("Ingresa el nombre del producto: ")

    while True:
        try:
            precio = float(input("Ingresa el precio del producto: "))
            if precio < 0:
                print("El precio no puede ser negativo. Intenta de nuevo.")
                continue
            break
        except ValueError:
            print("Por favor ingresa un número válido para el precio.")

    while True:
        try:
            unidades = int(input("Ingresa las unidades a solicitar: "))
            if unidades <= 0:
                print("Las unidades deben ser mayores a 0. Intenta de nuevo.")
                continue
            break
        except ValueError:
            print("Por favor ingresa un número entero válido para las unidades.")

    total = precio * unidades

    print("\n===== SIMULACIÓN DEL PEDIDO =====")
    print(f"Producto : {nombre_producto}")
    print(f"Precio   : ${precio:.2f}")
    print(f"Unidades : {unidades}")
    print("------------------------------")
    print(f"TOTAL A PAGAR: ${total:.2f}")
    print("=================================\n")

    return nombre_producto, total


def manejar_opcion(opcion, pedido_model):
    """
    Controla el flujo del programa dependiendo de la opción seleccionada.

    :param opcion: Letra seleccionada por el usuario.
    :param pedido_model: Instancia de la clase Pedido.
    :return: False si se debe salir, True si continúa el programa.
    """
    if opcion.lower() == "a":
        # Pedidos: cálculo simple + registro en BD con un nombre genérico de cliente
        nombre_producto, total = calcular_pedido_simple()
        cliente = input("Ingresa el nombre o clave del cliente para guardar el pedido: ")
        numero_pedido = pedido_model.crear_pedido(cliente, nombre_producto, total)
        print(f"Pedido guardado con número: {numero_pedido}")

    elif opcion.lower() == "b":
        print("\n[Clientes] Aquí se gestionarán los clientes (Avance 2 y 3).")

    elif opcion.lower() == "c":
        print("\n[Menú] Aquí se gestionará el menú de productos (Avance 2 y 3).")

    elif opcion.lower() == "d":
        print("\nSaliendo de Happy Burger... ¡Hasta luego!")
        return False

    else:
        print("\nOpción no válida. Intenta de nuevo.")

    return True


def main():
    """
    Función principal.

    - Inicializa la base de datos y las tablas.
    - Crea instancias de las clases principales.
    - Controla el ciclo del menú hasta que el usuario elija salir.
    """
    db = BaseDatos()
    db.crear_tablas()

    pedido_model = Pedido()
    # También podrías usar Clientes() y Menu() más adelante si quieres integrarlos en consola.

    continuar = True
    while continuar:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        continuar = manejar_opcion(opcion, pedido_model)


if __name__ == "__main__":
    main()
