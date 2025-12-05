"""
database.py
-----------
Módulo para gestionar la conexión y creación de la base de datos SQLite
para Happy Burger.
"""

import sqlite3
import os


class BaseDatos:
    """
    Clase BaseDatos
    ----------------
    Se encarga de manejar la conexión y la creación de tablas de la
    base de datos de Happy Burger.
    """

    def __init__(self, nombre_base_datos="happy_burger.db"):
        """
        Inicializa la clase con el nombre de la base de datos.

        :param nombre_base_datos: Nombre del archivo SQLite.
        """
        self.nombre_base_datos = nombre_base_datos

    def get_connection(self):
        """
        Devuelve una conexión a la base de datos y activa las claves foráneas.
        """
        conn = sqlite3.connect(self.nombre_base_datos)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def crear_tablas(self):
        """
        Crea las tablas Clientes, Menu y Pedido si no existen.
        """
        with self.get_connection() as conn:

            # Tabla Clientes
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clave TEXT NOT NULL UNIQUE,
                    nombre TEXT NOT NULL,
                    direccion TEXT,
                    correo_electronico TEXT,
                    telefono TEXT
                )
                """
            )

            # Tabla Menu
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Menu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clave TEXT NOT NULL UNIQUE,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL
                )
                """
            )

            # Tabla Pedido (con llaves foráneas correctas)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Pedido (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pedido INTEGER NOT NULL UNIQUE,
                    cliente TEXT NOT NULL,
                    producto TEXT NOT NULL,
                    precio REAL NOT NULL,

                    FOREIGN KEY (cliente) REFERENCES Clientes(clave) ON DELETE CASCADE,
                    FOREIGN KEY (producto) REFERENCES Menu(clave)
                )
                """
            )

            conn.commit()
