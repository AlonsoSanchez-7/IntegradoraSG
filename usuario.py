from conexionBD import conexion, cursor


class Usuario:
    def __init__(self, nombre, usuario, contrasena, rol="empleado", id_usuario=None):
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._usuario = usuario
        self._contrasena = contrasena
        self._rol = rol

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor):
        self._id_usuario = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        self._usuario = valor

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        self._contrasena = valor

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        self._rol = valor

    def es_admin(self):
        return self._rol.lower() == "admin"

    def insertar(self):
        try:
            cursor.execute(
                "INSERT INTO usuario (nombre, usuario, contrasena, rol) VALUES (%s, %s, %s, %s)",
                (self._nombre, self._usuario, self._contrasena, self._rol),
            )
            conexion.commit()
            return True
        except Exception:
            return False

    def actualizar(self, id_usuario):
        try:
            cursor.execute(
                "UPDATE usuario SET nombre=%s, usuario=%s, contrasena=%s, rol=%s WHERE id_usuario=%s",
                (self._nombre, self._usuario, self._contrasena, self._rol, id_usuario),
            )
            conexion.commit()
            return True
        except Exception:
            return False

    @staticmethod
    def eliminar(id_usuario):
        try:
            cursor.execute("DELETE FROM usuario WHERE id_usuario=%s", (id_usuario,))
            conexion.commit()
            return True
        except Exception:
            return False

    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT id_usuario, nombre, usuario, rol FROM usuario")
            return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def buscar(id_usuario):
        try:
            cursor.execute("SELECT * FROM usuario WHERE id_usuario=%s", (id_usuario,))
            return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def iniciar_sesion(usuario, contrasena):
        try:
            cursor.execute(
                "SELECT id_usuario, nombre, usuario, contrasena, rol FROM usuario WHERE usuario=%s AND contrasena=%s",
                (usuario, contrasena),
            )
            fila = cursor.fetchone()
            if fila:
                return Usuario(fila[1], fila[2], fila[3], fila[4], id_usuario=fila[0])
            return None
        except Exception:
            return None
