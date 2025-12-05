"""
pedido.py
---------
Módulo que contiene la clase Pedido para el manejo de pedidos
de Happy Burger usando SQLite.
"""

import os
from db.database import BaseDatos


class Pedido:
    """
    Clase Pedido
    ------------
    Administra los pedidos utilizando la tabla Pedido en SQLite.
    También permite generar un ticket en un archivo .txt y
    obtener información detallada mediante JOIN con Clientes y Menu.
    """

    def __init__(self, db_name="happy_burger.db", carpeta_tickets="tickets"):
        """
        Inicializa la clase Pedido con BaseDatos y la carpeta de tickets.

        :param db_name: Nombre del archivo de base de datos SQLite.
        :param carpeta_tickets: Carpeta donde se guardarán los tickets .txt.
        """
        self.db = BaseDatos(db_name)
        self.carpeta_tickets = carpeta_tickets
        os.makedirs(self.carpeta_tickets, exist_ok=True)

    def _obtener_siguiente_numero_pedido(self):
        """
        Obtiene el siguiente número de pedido consecutivo a partir de la tabla Pedido.

        :return: Siguiente número de pedido (integer).
        """
        with self.db.get_connection() as conn:
            fila = conn.execute("SELECT MAX(pedido) FROM Pedido").fetchone()
            max_pedido = fila[0] if fila and fila[0] is not None else 0
            return max_pedido + 1

    def crear_pedido(self, cliente, producto, precio):
        """
        Crear pedido.

        Inserta un nuevo pedido en la tabla Pedido y genera un ticket .txt.

        :param cliente: Clave o nombre del cliente (string).
        :param producto: Clave o nombre del producto (string).
        :param precio: Precio total del pedido (float).
        :return: Número de pedido generado (integer).
        """
        numero_pedido = self._obtener_siguiente_numero_pedido()

        with self.db.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO Pedido (pedido, cliente, producto, precio)
                VALUES (?, ?, ?, ?)
                """,
                (numero_pedido, cliente, producto, precio),
            )
            conn.commit()

        # Generar ticket en .txt
        self._generar_ticket(numero_pedido, cliente, producto, precio)
        return numero_pedido

    def cancelar_pedido(self, numero_pedido):
        """
        Cancelar pedido.

        Elimina un pedido de la tabla Pedido según su número.

        :param numero_pedido: Número del pedido a cancelar (integer).
        """
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM Pedido WHERE pedido = ?", (numero_pedido,))
            conn.commit()

    def obtener_por_numero(self, numero_pedido):
        """
        Obtiene un pedido por su número de pedido (sin JOIN).

        :param numero_pedido: Número del pedido (integer).
        :return: Fila con (pedido, cliente, producto, precio) o None si no existe.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT pedido, cliente, producto, precio
                FROM Pedido
                WHERE pedido = ?
                """,
                (numero_pedido,),
            ).fetchone()

    def obtener_todos(self):
        """
        Obtiene todos los pedidos sin detalle de JOIN.

        :return: Lista de filas con (pedido, cliente, producto, precio).
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT pedido, cliente, producto, precio FROM Pedido"
            ).fetchall()

    def obtener_todos_con_detalle(self):
        """
        Obtiene todos los pedidos haciendo JOIN con Clientes y Menu.

        Devuelve una lista de filas con:
        - numero_pedido
        - cliente_clave, cliente_nombre
        - producto_clave, producto_nombre
        - precio_producto (del menú)
        - total_pedido (precio guardado en la tabla Pedido)
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT
                    p.pedido               AS numero_pedido,
                    c.clave                AS cliente_clave,
                    c.nombre               AS cliente_nombre,
                    m.clave                AS producto_clave,
                    m.nombre               AS producto_nombre,
                    m.precio               AS precio_producto,
                    p.precio               AS total_pedido
                FROM Pedido AS p
                JOIN Clientes AS c ON p.cliente = c.clave
                JOIN Menu     AS m ON p.producto = m.clave
                ORDER BY p.pedido ASC
                """
            ).fetchall()

    def obtener_por_numero_con_detalle(self, numero_pedido):
        """
        Obtiene un pedido específico con detalle de cliente y producto,
        usando JOIN con las tablas Clientes y Menu.

        :param numero_pedido: Número consecutivo del pedido (integer).
        :return: Fila con:
                 (numero_pedido, cliente_clave, cliente_nombre,
                  producto_clave, producto_nombre, precio_producto, total_pedido)
                 o None si no existe.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT
                    p.pedido               AS numero_pedido,
                    c.clave                AS cliente_clave,
                    c.nombre               AS cliente_nombre,
                    m.clave                AS producto_clave,
                    m.nombre               AS producto_nombre,
                    m.precio               AS precio_producto,
                    p.precio               AS total_pedido
                FROM Pedido AS p
                JOIN Clientes AS c ON p.cliente = c.clave
                JOIN Menu     AS m ON p.producto = m.clave
                WHERE p.pedido = ?
                """,
                (numero_pedido,),
            ).fetchone()

    def _generar_ticket(self, numero_pedido, cliente, producto, precio):
        """
        Genera un archivo .txt que simula el ticket del pedido.

        :param numero_pedido: Número del pedido (integer).
        :param cliente: Nombre o clave del cliente (string).
        :param producto: Nombre o clave del producto (string).
        :param precio: Total del pedido (float).
        """
        ruta = os.path.join(self.carpeta_tickets, f"ticket_{numero_pedido}.txt")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("=== Happy Burger - Ticket de Pedido ===\n")
            f.write(f"Número de pedido: {numero_pedido}\n")
            f.write(f"Cliente: {cliente}\n")
            f.write(f"Producto: {producto}\n")
            f.write(f"Total a pagar: ${precio:.2f}\n")
            f.write("¡Gracias por tu compra en Happy Burger! 🍔\n")
