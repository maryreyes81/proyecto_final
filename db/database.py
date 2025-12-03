import sqlite3
import os

class BaseDatos:
    def __init__(self, nombreBaseDatos):
        self.nombreBaseDatos = nombreBaseDatos
    
    def crearBaseDatos(self):
        if not os.path.exists(self.nombreBaseDatos):
            conexion = sqlite3.connect(self.nombreBaseDatos)
            conexion.close()
            print(f"Base de datos '{self.nombreBaseDatos}' creada exitosamente.")
        else:
            print(f"La base de datos '{self.nombreBaseDatos}' ya existe.")
            
            # Crear tablas del restaurante
        self.crearTablaClientes()
        self.crearTablaMenu()
        self.crearTablaProducto()
        self.crearTablaMenuProducto()
        self.crearTablaPedidos()
        self.crearTablaPedidoDetalle()
            
        def get_connection(self):
                conn = sqlite3.connect(self.nombreBaseDatos)
                #Activar claves foráneas en SQLite
                conn.execute("PRAGMA foreign_keys = ON")
                return conn
             
        
        def crearTablaClientes(self): #Tabla principal
            with self.get_connection() as conexion:
             conexion.execute("""
            CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT UNIQUE,
                telefono TEXT,
                direccion TEXT
            )
        """)
             
    def crearTablaMenu(self):
        with self.get_connection() as conexion:
         conexion.execute("""
            CREATE TABLE IF NOT EXISTS Menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,              -- Ej: Desayunos, Comida, Cena
                descripcion TEXT,
                activo INTEGER NOT NULL DEFAULT 1
            )
        """)
         
    def crearTablaProducto(self):
         with self.get_connection() as conexion:
           conexion.execute("""
            CREATE TABLE IF NOT EXISTS Producto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,              -- Ej: Chilaquiles, Café, Tacos
                descripcion TEXT,
                precio REAL NOT NULL,
                categoria TEXT,                    -- Bebida, Platillo, Postre
                activo INTEGER NOT NULL DEFAULT 1
            )
        """)


    def crearTablaMenuProducto(self):
     with self.get_connection() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS MenuProducto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_id INTEGER NOT NULL,          -- FK → Menu(id)
                producto_id INTEGER NOT NULL,      -- FK → Producto(id)
                UNIQUE (menu_id, producto_id),
                FOREIGN KEY (menu_id) REFERENCES Menu(id) ON DELETE CASCADE,
                FOREIGN KEY (producto_id) REFERENCES Producto(id)
            )
        """)


           
    def crearTablaPedidos(self):
         with self.get_connection() as conexion:
           conexion.execute("""
            CREATE TABLE IF NOT EXISTS Pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,    -- FK → Clientes(id)
                cliente_id INTEGER NOT NULL, 
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'pendiente',
                description TEXT,
                total REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (cliente_id) REFERENCES Clientes(id) ON DELETE CASCADE
            )
        """)
           
    def crearTablaPedidoDetalle(self):
      with self.get_connection() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS PedidoDetalle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                pedido_id INTEGER NOT NULL,        -- FK → Pedidos(id)
                producto_id INTEGER NOT NULL,      -- FK → Producto(id)

                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,

                FOREIGN KEY (pedido_id) REFERENCES Pedidos(id) ON DELETE CASCADE,
                FOREIGN KEY (producto_id) REFERENCES Producto(id)
            )
        """)