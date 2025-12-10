"""
clientes.py
-----------
Modelo para el manejo de clientes de Happy Burger usando SQLite.
"""

from db.database import BaseDatos


class Clientes:
    """
    Clase Clientes
    --------------
    Administra los clientes utilizando la tabla Clientes en SQLite.
    """

    def __init__(self, db_name="happy_burger.db"):
        self.db = BaseDatos(db_name)

    def obtener_todos(self):
        """
        Obtiene todos los clientes registrados.
        Devuelve lista de tuplas: (id, nombre, direccion, correo_electronico, telefono)
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, nombre, direccion, correo_electronico, telefono
                FROM Clientes
                ORDER BY id
                """
            ).fetchall()

    def obtener_clientes(self):
        """
        Alias de obtener_todos para compatibilidad con otras partes del código.
        Devuelve lista de tuplas: (id, nombre, direccion, correo_electronico, telefono)
        """
        return self.obtener_todos()

    def obtener_por_id(self, cliente_id):
        """
        Obtiene un cliente por su ID.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, nombre, direccion, correo_electronico, telefono
                FROM Clientes
                WHERE id = ?
                """,
                (cliente_id,),
            ).fetchone()

    def agregar_cliente(self, nombre, direccion, correo_electronico, telefono):
        """
        Inserta un nuevo cliente en la tabla Clientes.
        """
        with self.db.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO Clientes (nombre, direccion, correo_electronico, telefono)
                VALUES (?, ?, ?, ?)
                """,
                (nombre, direccion, correo_electronico, telefono),
            )
            conn.commit()

    def actualizar_cliente(
        self,
        cliente_id,
        nombre=None,
        direccion=None,
        correo_electronico=None,
        telefono=None,
    ):
        """
        Actualiza los campos enviados para el cliente con el ID dado.
        Solo actualiza los campos que no sean None.
        """
        with self.db.get_connection() as conn:
            cliente = conn.execute(
                """
                SELECT id, nombre, direccion, correo_electronico, telefono
                FROM Clientes
                WHERE id = ?
                """,
                (cliente_id,),
            ).fetchone()

            if not cliente:
                return

            _, nombre_act, dir_act, correo_act, tel_act = cliente

            nuevo_nombre = nombre if nombre is not None else nombre_act
            nueva_dir = direccion if direccion is not None else dir_act
            nuevo_correo = (
                correo_electronico if correo_electronico is not None else correo_act
            )
            nuevo_tel = telefono if telefono is not None else tel_act

            conn.execute(
                """
                UPDATE Clientes
                SET nombre = ?, direccion = ?, correo_electronico = ?, telefono = ?
                WHERE id = ?
                """,
                (nuevo_nombre, nueva_dir, nuevo_correo, nuevo_tel, cliente_id),
            )
            conn.commit()

    def eliminar_cliente(self, cliente_id):
        """
        Elimina un cliente por su ID.
        """
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM Clientes WHERE id = ?", (cliente_id,))
            conn.commit()


