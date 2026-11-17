from conexionBD import conexion, cursor


class Cliente:
    def __init__(self, nombre, telefono="", id_cliente=None):
        self._id_cliente = id_cliente
        self._nombre = nombre
        self._telefono = telefono

    @property
    def id_cliente(self):
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, valor):
        self._id_cliente = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = valor

    def registrar(self):
        try:
            cursor.execute(
                "INSERT INTO cliente (nombre, telefono) VALUES (%s, %s)",
                (self._nombre, self._telefono),
            )
            conexion.commit()
            self._id_cliente = cursor.lastrowid
            return True
        except Exception:
            return False

    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT * FROM cliente")
            return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def buscar(id_cliente):
        try:
            cursor.execute("SELECT * FROM cliente WHERE id_cliente=%s", (id_cliente,))
            return cursor.fetchall()
        except Exception:
            return []
