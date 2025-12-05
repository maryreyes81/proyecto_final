def mostrar_menu():
    """
    Imprime en pantalla el menú principal con las opciones solicitadas.
    """
    print("\n==============================")
    print("      SISTEMA RESTAURANTE     ")
    print("==============================")
    print("a) Pedidos")
    print("b) Clientes")
    print("c) Menú")
    print("d) Salir")
    print("==============================")


def calcular_pedido():
    """
    Opción Pedidos:
    - Pide al usuario: nombre del producto, precio y unidades.
    - Calcula el costo total.
    - Imprime una simulación en pantalla.
    """
    print("\n--- Opción: Pedidos ---")

    nombre_producto = input("Ingresa el nombre del producto: ")

    # Pedir precio
    precio = float(input("Ingresa el precio del producto: "))
    # Pedir unidades
    unidades = int(input("Ingresa las unidades a solicitar: "))

    total = precio * unidades

    # Simulación en pantalla
    print("\n===== SIMULACIÓN DEL PEDIDO =====")
    print(f"Producto : {nombre_producto}")
    print(f"Precio   : ${precio:.2f}")
    print(f"Unidades : {unidades}")
    print("------------------------------")
    print(f"TOTAL A PAGAR: ${total:.2f}")
    print("=================================\n")


def manejar_opcion(opcion):
    """
    Controla el flujo del programa dependiendo de la opción seleccionada.
    Regresa False si el usuario quiere salir, True si debe continuar.
    """
    if opcion.lower() == "a":
        # Pedidos
        calcular_pedido()

    elif opcion.lower() == "b":
        # Clientes
        print("\nHas seleccionado la opción: Clientes.")
        print("Aquí se mostraría el manejo de clientes en futuras versiones.")

    elif opcion.lower() == "c":
        # Menú
        print("\nHas seleccionado la opción: Menú.")
        print("Aquí se mostraría el manejo del menú del restaurante.")

    elif opcion.lower() == "d":
        # Salir
        print("\nSaliendo del sistema... ¡Hasta luego!")
        return False

    else:
        print("\nOpción no válida. Intenta de nuevo.")

    return True


def main():
    """
    Función principal que muestra el menú y controla la iteración
    hasta que el usuario seleccione la opción Salir.
    """
    continuar = True
    while continuar:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        continuar = manejar_opcion(opcion)


if __name__ == "__main__":
    main()
