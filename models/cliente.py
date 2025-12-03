from db.database import BaseDatos

class Cliente:
  def __init__(self, db_name='db.sqlite3'):
    self.db = BaseDatos(db_name)
    
  def obtener_todos(self):
   with self.db.get_connection() as conn:
     return conn.execute("SELECT * FROM Clientes").fetchall()
 
  def obtener_por_id(self, cliente_id):
    with self.db.get_connection() as conn:
      return conn.execute(
          "SELECT * FROM Clientes WHERE id = ?", 
          (cliente_id,)
        ).fetchone()
      
    def crear(self, nombre, correo, telefono, direccion):
      with self.db.get_connection() as conn:
       conn.execute(
         "INSERT INTO Clientes (nombre, correo, telefono, direccion) VALUES (?, ?, ?, ?)",
            (nombre, correo, telefono, direccion)
          )
       conn.commit()
       
    def actualizar(self, cliente_id, nombre, correo, telefono, direccion):
      with self.db.get_connection() as conn:
        conn.execute(
          "UPDATE Clientes SET nombre = ?, correo = ?, telefono = ?, direccion = ? WHERE id = ?",
            (nombre, correo, telefono, direccion, cliente_id)
          )
        conn.commit()
        
    def eliminar(self, cliente_id):
      with self.db.get_connection() as conn:
        conn.execute(
          "DELETE FROM Clientes WHERE id = ?",
            (cliente_id,)
          )
        conn.commit()