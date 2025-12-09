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

    # =============================================================
    # INSERTAR CLIENTE
    # =============================================================
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

    # =============================================================
    # ELIMINAR CLIENTE
    # =============================================================
    def eliminar_cliente(self, clave):
        """
        Eliminar cliente por clave.
        """
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM Clientes WHERE clave = ?", (clave,))
            conn.commit()

    # =============================================================
    # ACTUALIZAR CLIENTE
    # =============================================================
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
                return  # No existe

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

    # =============================================================
    # OBTENER TODOS
    # =============================================================
    def obtener_todos(self):
        """
        Obtiene todos los clientes registrados.
        Retorna una lista de filas.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, clave, nombre, direccion, correo_electronico, telefono
                FROM Clientes
                """
            ).fetchall()

    # =============================================================
    # OBTENER POR ID
    # =============================================================
    def obtener_por_id(self, cliente_id):
        """
        Obtiene un cliente específico por su ID (PRIMARY KEY).
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

    # =============================================================
    # OBTENER POR CLAVE  ← MÉTODO QUE FALTABA
    # =============================================================
    def obtener_por_clave(self, clave):
        """
        Obtiene un cliente por su CLAVE (ej. 'C01').

        Retorna una fila con:
        (id, clave, nombre, direccion, correo_electronico, telefono)
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, clave, nombre, direccion, correo_electronico, telefono
                FROM Clientes
                WHERE clave = ?
                """,
                (clave,),
            ).fetchone()
