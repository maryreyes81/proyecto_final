"""
clientes.py
-----------
Módulo que contiene la clase Clientes para el manejo de clientes
de Happy Burger usando SQLite.
"""

from db.database import BaseDatos


class Clientes:
    """
    Clase Clientes
    --------------
    Administra los clientes utilizando la tabla Clientes en SQLite.
    """

    def __init__(self, db_name="happy_burger.db"):
        """
        Inicializa la clase Clientes con una instancia de BaseDatos.
        """
        self.db = BaseDatos(db_name)

    def agregar_cliente(self, clave, nombre, direccion, correo_electronico, telefono):
        """
        Agregar cliente.

        Inserta un nuevo cliente en la tabla Clientes.
        """
        with self.db.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO Clientes (clave, nombre, direccion, correo_electronico, telefono)
                VALUES (?, ?, ?, ?, ?)
                """,
                (clave, nombre, direccion, correo_electronico, telefono),
            )
            conn.commit()

    def eliminar_cliente(self, clave):
        """
        Eliminar cliente.

        Elimina un cliente por su clave.
        """
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM Clientes WHERE clave = ?", (clave,))
            conn.commit()

    def actualizar_cliente(
        self, clave, nombre=None, direccion=None, correo_electronico=None, telefono=None
    ):
        """
        Actualizar cliente.

        Actualiza los campos enviados para el cliente con la clave dada.
        """
        with self.db.get_connection() as conn:
            cliente = conn.execute(
                """
                SELECT id, nombre, direccion, correo_electronico, telefono
                FROM Clientes
                WHERE clave = ?
                """,
                (clave,),
            ).fetchone()

            if not cliente:
                return

            _, nombre_actual, dir_actual, correo_actual, tel_actual = cliente

            nuevo_nombre = nombre if nombre is not None else nombre_actual
            nueva_dir = direccion if direccion is not None else dir_actual
            nuevo_correo = (
                correo_electronico if correo_electronico is not None else correo_actual
            )
            nuevo_tel = telefono if telefono is not None else tel_actual

            conn.execute(
                """
                UPDATE Clientes
                SET nombre = ?, direccion = ?, correo_electronico = ?, telefono = ?
                WHERE clave = ?
                """,
                (nuevo_nombre, nueva_dir, nuevo_correo, nuevo_tel, clave),
            )
            conn.commit()

    def obtener_todos(self):
        """
        Obtiene todos los clientes registrados.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, clave, nombre, direccion, correo_electronico, telefono
                FROM Clientes
                """
            ).fetchall()

    def obtener_por_id(self, cliente_id):
        """
        Obtiene un cliente específico por su ID (PRIMARY KEY).

        :param cliente_id: ID numérico del cliente (integer).
        :return: Una fila con (id, clave, nombre, direccion, correo_electronico, telefono)
                 o None si no existe.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, clave, nombre, direccion, correo_electronico, telefono
                FROM Clientes
                WHERE id = ?
                """,
                (cliente_id,),
            ).fetchone()