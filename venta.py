from datetime import datetime, date
from conexionBD import conexion, cursor


class Venta:
    def __init__(self, usuario, cliente=None, id_venta=None, fecha=None):
        self._id_venta = id_venta
        self._fecha = fecha if fecha else datetime.now()
        self._total = 0.0
        self._items = []
        self._usuario = usuario
        self._cliente = cliente

    @property
    def id_venta(self):
        return self._id_venta

    @property
    def fecha(self):
        return self._fecha

    @property
    def total(self):
        return self._total

    @property
    def items(self):
        return self._items

    @property
    def usuario(self):
        return self._usuario

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        self._cliente = valor

    def agregar_item(self, producto, kg):
        if kg <= 0:
            raise ValueError("El peso debe ser mayor a 0 kg (RN-02).")
        kg_en_carrito = sum(k for p, k, _ in self._items if p.id_producto == producto.id_producto)
        if (kg + kg_en_carrito) > producto.stock_kg:
            raise ValueError(
                f"Stock insuficiente de {producto.nombre}. Disponible: {producto.stock_kg:.2f} kg."
            )
        subtotal = round(producto.precio_kg * kg, 2)
        self._items.append((producto, kg, subtotal))
        self.calcular_total()

    def limpiar_items(self):
        self._items.clear()
        self._total = 0.0

    def calcular_total(self):
        self._total = round(sum(sub for _, _, sub in self._items), 2)
        return self._total

    def registrar_venta(self):
        if not self._items:
            return False
        try:
            self._fecha = datetime.now()
            self.calcular_total()
            id_cli = self._cliente.id_cliente if self._cliente else None

            cursor.execute(
                "INSERT INTO venta (fecha, total, id_cliente, id_usuario) VALUES (%s, %s, %s, %s)",
                (self._fecha.strftime("%Y-%m-%d %H:%M:%S"), self._total, id_cli, self._usuario.id_usuario),
            )
            self._id_venta = cursor.lastrowid

            for prod, kg, subtotal in self._items:
                cursor.execute(
                    """INSERT INTO detalle_venta (id_venta, id_producto, cantidad_kg, precio_kg, subtotal) 
                    VALUES (%s, %s, %s, %s, %s)""",
                    (self._id_venta, prod.id_producto, kg, prod.precio_kg, subtotal),
                )
                cursor.execute(
                    "UPDATE producto SET stock_kg = stock_kg - %s WHERE id_producto = %s",
                    (kg, prod.id_producto),
                )
                prod.stock_kg -= kg

            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            print("Error al registrar venta:", e)
            return False

    def generar_recibo(self):
        lineas = [
            "====================================",
            "          CARNICERÍA S.G.           ",
            " Con el producto y atención que ud. ",
            "              merece                ",
            "====================================",
            f"Ticket No. : {self._id_venta}",
            f"Fecha      : {self._fecha.strftime('%d/%m/%Y %H:%M')}",
            f"Atendió    : {self._usuario.nombre}",
        ]
        if self._cliente:
            lineas.append(f"Cliente    : {self._cliente.nombre}")
        lineas.append("------------------------------------")
        for prod, kg, subtotal in self._items:
            lineas.append(f"{prod.nombre}")
            lineas.append(f"  {kg:.3f} kg x ${prod.precio_kg:.2f} = ${subtotal:.2f}")
        lineas.append("------------------------------------")
        lineas.append(f"TOTAL A PAGAR: ${self._total:.2f} MXN")
        lineas.append("====================================")
        return "\n".join(lineas)

    @staticmethod
    def generar_corte(fecha_str=None):
        if not fecha_str:
            fecha_str = date.today().strftime("%Y-%m-%d")
        try:
            cursor.execute(
                """SELECT v.id_venta, v.fecha, u.nombre, IFNULL(c.nombre, 'Público General'), v.total
                FROM venta v
                JOIN usuario u ON v.id_usuario = u.id_usuario
                LEFT JOIN cliente c ON v.id_cliente = c.id_cliente
                WHERE DATE(v.fecha) = %s
                ORDER BY v.fecha DESC""",
                (fecha_str,),
            )
            ventas = cursor.fetchall()
            total_dia = sum(v[4] for v in ventas)
            return ventas, round(total_dia, 2)
        except Exception:
            return [], 0.0
