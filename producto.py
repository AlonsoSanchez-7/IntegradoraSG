from datetime import date, datetime
from conexionBD import conexion, cursor


class Producto:
    def __init__(
        self,
        nombre,
        descripcion,
        precio_kg,
        stock_kg,
        stock_minimo,
        fecha_caducidad,
        id_producto=None,
    ):
        self._id_producto = id_producto
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio_kg = float(precio_kg)
        self._stock_kg = float(stock_kg)
        self._stock_minimo = float(stock_minimo)
        self._fecha_caducidad = fecha_caducidad

    @property
    def id_producto(self):
        return self._id_producto

    @id_producto.setter
    def id_producto(self, valor):
        self._id_producto = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = valor

    @property
    def precio_kg(self):
        return self._precio_kg

    @precio_kg.setter
    def precio_kg(self, valor):
        self._precio_kg = float(valor)

    @property
    def stock_kg(self):
        return self._stock_kg

    @stock_kg.setter
    def stock_kg(self, valor):
        self._stock_kg = float(valor)

    @property
    def stock_minimo(self):
        return self._stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, valor):
        self._stock_minimo = float(valor)

    @property
    def fecha_caducidad(self):
        return self._fecha_caducidad

    @fecha_caducidad.setter
    def fecha_caducidad(self, valor):
        self._fecha_caducidad = valor

    def alerta_caducidad(self):
        fecha_cad = self._fecha_caducidad
        if isinstance(fecha_cad, str):
            fecha_cad = datetime.strptime(fecha_cad, "%Y-%m-%d").date()
        dias = (fecha_cad - date.today()).days
        if dias < 0:
            return f"¡CADUCADO hace {abs(dias)} día(s)!"
        if dias <= 2:
            return f"¡POR CADUCAR en {dias} día(s)!"
        return "Caducidad OK"

    def alerta_stock(self):
        if self._stock_kg <= 0:
            return "AGOTADO (0 kg)"
        if self._stock_kg <= self._stock_minimo:
            return f"STOCK BAJO (Mín: {self._stock_minimo} kg)"
        return "Stock OK"

    def insertar(self):
        try:
            cursor.execute(
                """INSERT INTO producto 
                (nombre, descripcion, precio_kg, stock_kg, stock_minimo, fecha_caducidad) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    self._nombre,
                    self._descripcion,
                    self._precio_kg,
                    self._stock_kg,
                    self._stock_minimo,
                    self._fecha_caducidad,
                ),
            )
            conexion.commit()
            return True
        except Exception:
            return False

    def actualizar(self, id_producto):
        try:
            cursor.execute(
                """UPDATE producto SET nombre=%s, descripcion=%s, precio_kg=%s, 
                stock_kg=%s, stock_minimo=%s, fecha_caducidad=%s WHERE id_producto=%s""",
                (
                    self._nombre,
                    self._descripcion,
                    self._precio_kg,
                    self._stock_kg,
                    self._stock_minimo,
                    self._fecha_caducidad,
                    id_producto,
                ),
            )
            conexion.commit()
            return True
        except Exception:
            return False

    @staticmethod
    def eliminar(id_producto):
        try:
            cursor.execute("DELETE FROM producto WHERE id_producto=%s", (id_producto,))
            conexion.commit()
            return True
        except Exception:
            return False

    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT * FROM producto")
            return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def buscar(id_producto):
        try:
            cursor.execute("SELECT * FROM producto WHERE id_producto=%s", (id_producto,))
            return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def registrar_entrada(id_producto, kg_recibidos, nueva_caducidad):
        try:
            cursor.execute(
                "UPDATE producto SET stock_kg = stock_kg + %s, fecha_caducidad = %s WHERE id_producto = %s",
                (float(kg_recibidos), nueva_caducidad, id_producto),
            )
            conexion.commit()
            return True
        except Exception:
            return False

    @staticmethod
    def registrar_merma(id_producto, kg_merma):
        try:
            cursor.execute(
                "UPDATE producto SET stock_kg = GREATEST(0, stock_kg - %s) WHERE id_producto = %s",
                (float(kg_merma), id_producto),
            )
            conexion.commit()
            return True
        except Exception:
            return False
