from datetime import date, timedelta
from tkinter import (
    Tk,
    Frame,
    Label,
    Entry,
    Button,
    messagebox,
    ttk,
    END,
    Canvas,
    PhotoImage,
)
import os

from usuario import Usuario
from cliente import Cliente
from producto import Producto
from venta import Venta

COLOR_GUINDA = "#7A1C1C"
COLOR_CREMA = "#FAF2DB"
COLOR_BLANCO = "#FFFFFF"
COLOR_BOTON = "#4A6B53"
COLOR_BOTON_HOVER = "#3B5542"
COLOR_TEXTO = "#2B2B2B"
COLOR_BORDE = "#C5BCA0"

CLAVE_CORTE_DUENO = "vibes2026"


class AppCarniceria:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Carnicería S.G. - Sistema de Ventas e Inventario")
        self.ventana.geometry("900x740")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg=COLOR_CREMA)

        self.usuario_actual = None
        self.venta_actual = None

        self.logo_img_small = None
        self.logo_img_large = None
        if os.path.exists("logo_carniceria.png"):
            try:
                self.logo_img_small = PhotoImage(file="logo_carniceria.png")
            except Exception:
                pass

        self.pantalla_carga_view()

    def borrar_pantalla(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    def dibujar_barra_superior(self, mostrar_menu=False, comando_menu=None):
        barra_top = Frame(self.ventana, bg=COLOR_GUINDA, height=45)
        barra_top.pack(fill="x")
        barra_top.pack_propagate(False)

        if self.logo_img_small:
            try:
                logo_mini = self.logo_img_small.subsample(12, 12)
                logo_lbl = Label(barra_top, image=logo_mini, bg=COLOR_GUINDA)
                logo_lbl.image = logo_mini
                logo_lbl.pack(side="left", padx=10, pady=4)
            except Exception:
                pass
        else:
            Label(barra_top, text=" 🐂 SG ", bg=COLOR_BLANCO, fg=COLOR_GUINDA, font=("Georgia", 11, "bold")).pack(side="left", padx=12, pady=8)

        if mostrar_menu and comando_menu:
            btn_menu = Button(
                barra_top,
                text="Menú",
                command=comando_menu,
                bg="#4A2525",
                fg=COLOR_BLANCO,
                font=("Georgia", 9, "bold"),
                relief="flat",
                cursor="hand2",
            )
            btn_menu.pack(side="left", padx=5, pady=8)

        if self.usuario_actual:
            Label(
                barra_top,
                text=f"Usuario: {self.usuario_actual.nombre} ({self.usuario_actual.rol.upper()})",
                bg=COLOR_GUINDA,
                fg=COLOR_BLANCO,
                font=("Segoe UI", 9, "bold"),
            ).pack(side="right", padx=15)

    def dibujar_titulo_encabezado_principal(self, fondo=COLOR_CREMA):
        marco_titulo = Frame(
            self.ventana,
            bg=fondo,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1,
            padx=45,
            pady=12,
        )
        marco_titulo.pack(pady=(20, 12))

        Label(
            marco_titulo,
            text="CARNICERIA S.G.",
            bg=fondo,
            fg=COLOR_TEXTO,
            font=("Georgia", 18, "bold"),
        ).pack()

        Label(
            marco_titulo,
            text="Con el producto y la atención que usted se merece",
            bg=fondo,
            fg="#4A4538",
            font=("Georgia", 10, "italic"),
        ).pack(pady=(2, 0))

    def dibujar_titulo_seccion(self, texto_titulo):
        marco_tit = Frame(
            self.ventana,
            bg=COLOR_GUINDA,
            padx=20,
            pady=6,
        )
        marco_tit.pack(pady=(12, 10), fill="x", padx=40)

        Label(
            marco_tit,
            text=texto_titulo,
            bg=COLOR_GUINDA,
            fg=COLOR_BLANCO,
            font=("Georgia", 14, "bold"),
        ).pack()

    def crear_boton(self, padre, texto, comando, ancho=18, alto=1, fuente=("Georgia", 10)):
        return Button(
            padre,
            text=texto,
            command=comando,
            bg=COLOR_BOTON,
            fg=COLOR_BLANCO,
            activebackground=COLOR_BOTON_HOVER,
            activeforeground=COLOR_BLANCO,
            font=fuente,
            width=ancho,
            height=alto,
            relief="flat",
            cursor="hand2",
        )

    def pantalla_carga_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_GUINDA)

        centro = Frame(self.ventana, bg=COLOR_GUINDA)
        centro.pack(expand=True)

        if os.path.exists("logo_carniceria.png"):
            try:
                self.logo_img_large = PhotoImage(file="logo_carniceria.png")
                lbl_img = Label(centro, image=self.logo_img_large, bg=COLOR_GUINDA)
                lbl_img.pack(pady=15)
            except Exception:
                pass

        Label(
            centro,
            text="CARNICERÍA S.G.",
            bg=COLOR_GUINDA,
            fg=COLOR_BLANCO,
            font=("Georgia", 24, "bold"),
        ).pack(pady=10)

        Label(
            centro,
            text="Cargando sistema, por favor espere...",
            bg=COLOR_GUINDA,
            fg="#F3E5AB",
            font=("Georgia", 11, "italic"),
        ).pack(pady=5)

        self.ventana.after(2500, self.login_view)

    def login_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_CREMA)
        self.usuario_actual = None

        Frame(self.ventana, bg=COLOR_GUINDA, height=45).pack(fill="x")
        self.dibujar_titulo_encabezado_principal(fondo=COLOR_CREMA)

        Label(self.ventana, text="INICIAR SESIÓN", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Georgia", 12, "bold")).pack(pady=(5, 10))

        form = Frame(self.ventana, bg=COLOR_CREMA)
        form.pack()

        Label(form, text="Usuario:", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Segoe UI", 10)).pack(anchor="w")
        self.ent_login_user = Entry(form, width=32, font=("Segoe UI", 10), relief="solid", bd=1)
        self.ent_login_user.focus()
        self.ent_login_user.pack(pady=(2, 10), ipady=2)

        Label(form, text="Contraseña:", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Segoe UI", 10)).pack(anchor="w")
        self.ent_login_pass = Entry(form, width=32, font=("Segoe UI", 10), show="*", relief="solid", bd=1)
        self.ent_login_pass.pack(pady=(2, 15), ipady=2)

        self.crear_boton(self.ventana, "Iniciar sesión", self.login_controller, ancho=16).pack(pady=4)
        self.crear_boton(self.ventana, "Registrar", self.registro_view, ancho=16).pack(pady=4)
        self.crear_boton(self.ventana, "Salir", self.ventana.quit, ancho=16).pack(pady=4)

    def registro_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_CREMA)

        Frame(self.ventana, bg=COLOR_GUINDA, height=45).pack(fill="x")
        self.dibujar_titulo_encabezado_principal(fondo=COLOR_CREMA)

        Label(self.ventana, text="REGISTRARSE:", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Georgia", 12, "bold")).pack(pady=(5, 10))

        form = Frame(self.ventana, bg=COLOR_CREMA)
        form.pack()

        Label(form, text="Usuario:", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Segoe UI", 10)).pack(anchor="w")
        self.reg_user = Entry(form, width=32, font=("Segoe UI", 10), relief="solid", bd=1)
        self.reg_user.focus()
        self.reg_user.pack(pady=(2, 10), ipady=2)

        Label(form, text="Contraseña:", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Segoe UI", 10)).pack(anchor="w")
        self.reg_pass = Entry(form, width=32, font=("Segoe UI", 10), show="*", relief="solid", bd=1)
        self.reg_pass.pack(pady=(2, 10), ipady=2)

        Label(form, text="Confirmar contraseña:", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Segoe UI", 10)).pack(anchor="w")
        self.reg_pass2 = Entry(form, width=32, font=("Segoe UI", 10), show="*", relief="solid", bd=1)
        self.reg_pass2.pack(pady=(2, 15), ipady=2)

        self.crear_boton(self.ventana, "Registrarse", self.registro_controller, ancho=16).pack(pady=4)
        self.crear_boton(self.ventana, "Regresar", self.login_view, ancho=16).pack(pady=4)

    def menu_principal_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_BLANCO)
        self.dibujar_barra_superior(mostrar_menu=False)
        self.dibujar_titulo_encabezado_principal(fondo=COLOR_BLANCO)

        contenedor = Frame(self.ventana, bg=COLOR_BLANCO)
        contenedor.pack(pady=12)

        if self.usuario_actual and self.usuario_actual.es_admin():
            self.crear_boton(contenedor, "Administracion", self.administracion_view, ancho=28, alto=1, fuente=("Georgia", 13)).pack(pady=6, ipady=3)

        self.crear_boton(contenedor, "Productos", self.productos_view, ancho=28, alto=1, fuente=("Georgia", 13)).pack(pady=6, ipady=3)
        self.crear_boton(contenedor, "Inventario", self.consultar_inventario_view, ancho=28, alto=1, fuente=("Georgia", 13)).pack(pady=6, ipady=3)
        self.crear_boton(contenedor, "Corte", self.verificar_clave_corte_view, ancho=28, alto=1, fuente=("Georgia", 13)).pack(pady=6, ipady=3)
        self.crear_boton(contenedor, "Ventas", self.ventas_view, ancho=28, alto=1, fuente=("Georgia", 13)).pack(pady=6, ipady=3)

        self.crear_boton(self.ventana, "Salir", self.login_view, ancho=14, fuente=("Georgia", 9)).pack(pady=10)

    def verificar_clave_corte_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_CREMA)

        Frame(self.ventana, bg=COLOR_GUINDA, height=45).pack(fill="x")
        Label(self.ventana, text="", bg=COLOR_CREMA).pack(pady=30)

        Label(self.ventana, text="--------------------------------------------------------", bg=COLOR_CREMA, fg="#2B2B2B", font=("Consolas", 11, "bold")).pack(pady=4)
        Label(self.ventana, text="Por favor introduce la contraseña", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Georgia", 16)).pack(pady=10)
        Label(self.ventana, text="--------------------------------------------------------", bg=COLOR_CREMA, fg="#2B2B2B", font=("Consolas", 11, "bold")).pack(pady=4)

        self.ent_clave_corte = Entry(self.ventana, width=28, font=("Segoe UI", 12), show="*", justify="center", relief="solid", bd=1)
        self.ent_clave_corte.focus()
        self.ent_clave_corte.pack(pady=(25, 20), ipady=4)
        self.ent_clave_corte.bind("<Return>", lambda event: self.validar_clave_corte_controller())

        self.crear_boton(self.ventana, "Confirmar", self.validar_clave_corte_controller, ancho=15).pack(pady=6)
        self.crear_boton(self.ventana, "Regresar", self.menu_principal_view, ancho=15).pack(pady=6)

        Frame(self.ventana, bg=COLOR_GUINDA, height=45).pack(side="bottom", fill="x")

    def validar_clave_corte_controller(self):
        if self.ent_clave_corte.get().strip() == CLAVE_CORTE_DUENO:
            self.corte_caja_view()
        else:
            messagebox.showerror("Acceso Denegado", "Contraseña incorrecta. Solo el dueño puede acceder al Corte.")
            self.ent_clave_corte.delete(0, END)

    # ==========================================================
    # 4. MÓDULO PRODUCTOS (Desktop-1: Formulario con inputs para registrar)
    # ==========================================================
    def productos_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_CREMA)
        self.dibujar_barra_superior(mostrar_menu=True, comando_menu=self.menu_principal_view)
        self.dibujar_titulo_seccion("REGISTRO DE PRODUCTOS")

        frm_tabla = Frame(self.ventana, bg=COLOR_CREMA)
        frm_tabla.pack(pady=10, padx=40, fill="x")

        campos_prod = [
            "*Nombre:",
            "*Cantidad:",
            "*Precio:",
            "Fecha de compra:",
            "Fecha estimada de caducidad:",
            "Proveedor:",
            "Unidad:",
        ]

        self.entradas_prod = {}
        for campo in campos_prod:
            fila = Frame(frm_tabla, bg="#FAF2DB", relief="solid", bd=1)
            fila.pack(pady=3, fill="x")
            
            lbl = Label(fila, text=f"  {campo}", width=30, anchor="w", bg="#E8E1CC", font=("Segoe UI", 9, "bold"))
            lbl.pack(side="left", fill="y", padx=(0, 10))

            ent = Entry(fila, width=45, relief="flat", bg=COLOR_BLANCO, font=("Segoe UI", 10))
            if campo == "Fecha de compra:":
                ent.insert(0, str(date.today()))
            elif campo == "Fecha estimada de caducidad:":
                ent.insert(0, str(date.today() + timedelta(days=5)))
            elif campo == "Unidad:":
                ent.insert(0, "Kg")
            ent.pack(side="left", padx=10, pady=4, ipady=2, fill="x", expand=True)
            self.entradas_prod[campo] = ent

        btn_pie = Frame(self.ventana, bg=COLOR_CREMA)
        btn_pie.pack(pady=15)
        self.crear_boton(btn_pie, "Registrar", self.guardar_producto_controller, ancho=18).pack(side="left", padx=10)
        self.crear_boton(btn_pie, "Regresar", self.menu_principal_view, ancho=18).pack(side="left", padx=10)

    def guardar_producto_controller(self):
        try:
            nombre = self.entradas_prod["*Nombre:"].get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre del producto es obligatorio.")
                return
            stock = float(self.entradas_prod["*Cantidad:"].get().strip())
            precio = float(self.entradas_prod["*Precio:"].get().strip())
            cad = self.entradas_prod["Fecha estimada de caducidad:"].get().strip() or str(date.today() + timedelta(days=5))
            
            # Proveedor opcional (si no se pone nada o no hay proveedores, se asigna 'General')
            prov = self.entradas_prod["Proveedor:"].get().strip()
            if not prov:
                prov = "General"

            p = Producto(nombre, prov, precio, stock, 5.0, cad)
            if p.insertar():
                messagebox.showinfo("Éxito", "Producto registrado correctamente.")
                self.productos_view()
            else:
                messagebox.showerror("Error", "No se pudo registrar el producto.")
        except ValueError:
            messagebox.showerror("Error", "Verifica que Cantidad y Precio sean numéricos.")

    # ==========================================================
    # 5. MÓDULO INVENTARIO (Consulta general)
    # ==========================================================
    def consultar_inventario_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_CREMA)
        self.dibujar_barra_superior(mostrar_menu=True, comando_menu=self.menu_principal_view)
        self.dibujar_titulo_seccion("INVENTARIO DE PRODUCTOS")

        frm_lista = Frame(self.ventana, bg=COLOR_CREMA)
        frm_lista.pack(pady=10, padx=30, fill="both", expand=True)

        cols = ("ID", "Nombre", "Proveedor/Corte", "Precio/Kg", "Stock (Kg)", "Caducidad", "Estado")
        tabla = ttk.Treeview(self.ventana, columns=cols, show="headings", height=12)
        anchos = [45, 160, 150, 90, 90, 100, 175]
        for c, a in zip(cols, anchos):
            tabla.heading(c, text=c)
            tabla.column(c, width=a, anchor="center")
        tabla.pack(pady=5, padx=25, fill="both", expand=True)

        for p_data in Producto.consultar():
            p = Producto(p_data[1], p_data[2], p_data[3], p_data[4], p_data[5], p_data[6], id_producto=p_data[0])
            estado = f"{p.alerta_stock()} | {p.alerta_caducidad()}"
            tabla.insert("", END, values=(p.id_producto, p.nombre, p.descripcion, f"${p.precio_kg:.2f}", f"{p.stock_kg:.2f}", p.fecha_caducidad, estado))

        btn_pie = Frame(self.ventana, bg=COLOR_CREMA)
        btn_pie.pack(pady=15)
        self.crear_boton(btn_pie, "Regresar", self.productos_view, ancho=18).pack()

    # ==========================================================
    # 6. MÓDULO ADMINISTRACIÓN (Listado con Botones Verdes Modificar)
    # ==========================================================
    def administracion_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_CREMA)
        self.dibujar_barra_superior(mostrar_menu=True, comando_menu=self.menu_principal_view)
        self.dibujar_titulo_seccion("ADMINISTRACIÓN DE PRODUCTOS")

        # Barra de búsqueda mejorada con etiqueta explícita
        frm_busq = Frame(self.ventana, bg=COLOR_CREMA)
        frm_busq.pack(pady=8, anchor="w", padx=40)
        
        Label(frm_busq, text="Buscar producto:", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 5))
        
        self.ent_busqueda_admin = Entry(frm_busq, width=32, relief="solid", bd=1, font=("Segoe UI", 10))
        self.ent_busqueda_admin.pack(side="left", padx=5, ipady=3)
        self.ent_busqueda_admin.bind("<KeyRelease>", lambda event: self.filtrar_administracion_controller())
        self.ent_busqueda_admin.bind("<Return>", lambda event: self.filtrar_administracion_controller())

        self.crear_boton(frm_busq, "Buscar", self.filtrar_administracion_controller, ancho=10, fuente=("Georgia", 9)).pack(side="left", padx=8)

        # Contenedor de la lista con Scrollbar
        self.frm_lista_admin = Frame(self.ventana, bg=COLOR_CREMA)
        self.frm_lista_admin.pack(pady=8, padx=30, fill="both", expand=True)

        self.cargar_lista_administracion()

        btn_pie = Frame(self.ventana, bg=COLOR_CREMA)
        btn_pie.pack(pady=10)
        self.crear_boton(btn_pie, "Regresar al Menú", self.menu_principal_view, ancho=20).pack()

    def cargar_lista_administracion(self, filtro=""):
        for widget in self.frm_lista_admin.winfo_children():
            widget.destroy()

        canvas = Canvas(self.frm_lista_admin, bg=COLOR_CREMA, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frm_lista_admin, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=COLOR_CREMA)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        productos = Producto.consultar()
        filtro = filtro.lower().strip()
        
        encontrados = 0
        for p_data in productos:
            p = Producto(p_data[1], p_data[2], p_data[3], p_data[4], p_data[5], p_data[6], id_producto=p_data[0])
            
            # Aplicar filtro si se escribió algo en el input de búsqueda
            if filtro and filtro not in p.nombre.lower() and filtro not in str(p.id_producto) and filtro not in p.descripcion.lower():
                continue

            encontrados += 1
            fila_item = Frame(scrollable_frame, bg="#E8E1CC", relief="solid", bd=1, width=825, height=48)
            fila_item.pack(pady=4, fill="x")
            fila_item.pack_propagate(False)

            info_txt = f" ID: {p.id_producto} | {p.nombre} | ${p.precio_kg:.2f}/kg | Stock: {p.stock_kg:.2f}kg | Cad: {p.fecha_caducidad}"
            Label(fila_item, text=info_txt, bg="#E8E1CC", fg=COLOR_TEXTO, font=("Segoe UI", 9, "bold")).pack(side="left", padx=12)

            btn_mod = Button(
                fila_item,
                text="Modificar",
                command=lambda id_p=p.id_producto: self.modificar_producto_prompt(id_p),
                bg=COLOR_BOTON,
                fg=COLOR_BLANCO,
                activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_BLANCO,
                font=("Georgia", 9, "bold"),
                width=12,
                relief="flat",
                cursor="hand2",
            )
            btn_mod.pack(side="right", padx=12, pady=8)

        if encontrados == 0:
            Label(scrollable_frame, text="No se encontraron productos coincidentes.", bg=COLOR_CREMA, fg=COLOR_TEXTO, font=("Segoe UI", 10)).pack(pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def filtrar_administracion_controller(self):
        texto_busq = self.ent_busqueda_admin.get()
        self.cargar_lista_administracion(texto_busq)

    def modificar_producto_prompt(self, id_producto):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_CREMA)
        self.dibujar_barra_superior(mostrar_menu=True, comando_menu=self.administracion_view)
        self.dibujar_titulo_seccion(f"MODIFICAR PRODUCTO (ID: {id_producto})")

        prod_data = Producto.buscar(id_producto)
        if not prod_data:
            messagebox.showerror("Error", "No se encontró el producto.")
            self.administracion_view()
            return
        
        p_info = prod_data[0]

        frm_tabla = Frame(self.ventana, bg=COLOR_CREMA)
        frm_tabla.pack(pady=15, padx=40, fill="x")

        campos_mod = [
            ("*Nombre:", p_info[1]),
            ("*Cantidad (Stock kg):", str(p_info[4])),
            ("*Precio ($/kg):", str(p_info[3])),
            ("Proveedor / Descripción:", p_info[2]),
            ("Fecha estimada de caducidad:", str(p_info[6])),
        ]

        self.entradas_mod = {}
        for campo, val_actual in campos_mod:
            fila = Frame(frm_tabla, bg="#FAF2DB", relief="solid", bd=1)
            fila.pack(pady=3, fill="x")
            
            lbl = Label(fila, text=f"  {campo}", width=32, anchor="w", bg="#E8E1CC", font=("Segoe UI", 9, "bold"))
            lbl.pack(side="left", fill="y", padx=(0, 10))

            ent = Entry(fila, width=40, relief="flat", bg=COLOR_BLANCO, font=("Segoe UI", 10))
            ent.insert(0, str(val_actual))
            ent.pack(side="left", padx=10, pady=4, ipady=2, fill="x", expand=True)
            self.entradas_mod[campo] = ent

        btn_pie = Frame(self.ventana, bg=COLOR_CREMA)
        btn_pie.pack(pady=15)
        self.crear_boton(btn_pie, "Guardar Cambios", lambda: self.guardar_modificacion_controller(id_producto), ancho=18).pack(side="left", padx=10)
        self.crear_boton(btn_pie, "Cancelar", self.administracion_view, ancho=18).pack(side="left", padx=10)

    def guardar_modificacion_controller(self, id_producto):
        try:
            nombre = self.entradas_mod["*Nombre:"].get().strip()
            stock = float(self.entradas_mod["*Cantidad (Stock kg):"].get().strip())
            precio = float(self.entradas_mod["*Precio ($/kg):"].get().strip())
            desc = self.entradas_mod["Proveedor / Descripción:"].get().strip()
            cad = self.entradas_mod["Fecha estimada de caducidad:"].get().strip()

            p = Producto(nombre, desc, precio, stock, 5.0, cad, id_producto=id_producto)
            if p.actualizar(id_producto):
                messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                self.administracion_view()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto en la base de datos.")
        except ValueError:
            messagebox.showerror("Error", "Verifica que Cantidad y Precio sean valores numéricos válidos.")

    def ventas_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_CREMA)
        self.dibujar_barra_superior(mostrar_menu=True, comando_menu=self.menu_principal_view)
        self.dibujar_titulo_seccion("VENTAS")

        if not self.venta_actual:
            self.venta_actual = Venta(usuario=self.usuario_actual)

        frm_cap = Frame(self.ventana, bg=COLOR_CREMA)
        frm_cap.pack(pady=6)

        self.productos_disponibles = {}
        opciones = []
        for f in Producto.consultar():
            prod = Producto(f[1], f[2], f[3], f[4], f[5], f[6], id_producto=f[0])
            etiq = f"{prod.id_producto} - {prod.nombre} (${prod.precio_kg:.2f}/kg | Disp: {prod.stock_kg:.2f} kg)"
            self.productos_disponibles[etiq] = prod
            opciones.append(etiq)

        Label(frm_cap, text="Producto:", bg=COLOR_CREMA, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=4)
        self.cb_venta_prod = ttk.Combobox(frm_cap, values=opciones, state="readonly", width=38)
        if opciones:
            self.cb_venta_prod.current(0)
        self.cb_venta_prod.grid(row=0, column=1, padx=4)

        Label(frm_cap, text="Kg (Input):", bg=COLOR_CREMA, font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=4)
        self.ent_venta_kg = Entry(frm_cap, width=12, relief="solid", bd=1, font=("Segoe UI", 10))
        self.ent_venta_kg.grid(row=0, column=3, padx=4)

        self.crear_boton(frm_cap, "+ Agregar", self.agregar_item_venta_controller, ancho=12, fuente=("Georgia", 9)).grid(row=0, column=4, padx=6)

        cols = ("Clave", "Producto", "Corte", "Cantidad", "Subtotal")
        self.tabla_ventas = ttk.Treeview(self.ventana, columns=cols, show="headings", height=10)
        anchos = [90, 190, 160, 110, 120]
        for c, a in zip(cols, anchos):
            self.tabla_ventas.heading(c, text=c)
            self.tabla_ventas.column(c, width=a, anchor="center")
        self.tabla_ventas.pack(pady=8, padx=25)

        self.refrescar_tabla_ventas()

        frm_total = Frame(self.ventana, bg=COLOR_CREMA)
        frm_total.pack(anchor="e", padx=45, pady=2)
        Label(frm_total, text="TOTAL:", bg=COLOR_CREMA, font=("Georgia", 11, "bold")).pack(side="left", padx=5)
        self.lbl_total_v = Label(frm_total, text="$0.00", bg="#E8E1CC", width=15, relief="solid", bd=1, font=("Georgia", 11, "bold"))
        self.lbl_total_v.pack(side="left")

        btn_pie = Frame(self.ventana, bg=COLOR_CREMA)
        btn_pie.pack(pady=10)
        self.crear_boton(btn_pie, "Registrar Venta", self.cobrar_venta_controller, ancho=18).pack(side="left", padx=10)
        self.crear_boton(btn_pie, "Regresar", self.menu_principal_view, ancho=18).pack(side="left", padx=10)

    def agregar_item_venta_controller(self):
        sel = self.cb_venta_prod.get()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return
        try:
            kg = float(self.ent_venta_kg.get())
            prod = self.productos_disponibles[sel]
            self.venta_actual.agregar_item(prod, kg)
            self.ent_venta_kg.delete(0, END)
            self.refrescar_tabla_ventas()
        except ValueError as e:
            messagebox.showerror("Validación", str(e))

    def refrescar_tabla_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for prod, kg, sub in self.venta_actual.items:
            self.tabla_ventas.insert(
                "", END, values=(prod.id_producto, prod.nombre, prod.descripcion or "Corte", f"{kg:.2f} kg", f"${sub:.2f}")
            )
        if hasattr(self, "lbl_total_v"):
            self.lbl_total_v.config(text=f"${self.venta_actual.calcular_total():.2f}")

    def cobrar_venta_controller(self):
        if not self.venta_actual.items:
            messagebox.showwarning("Venta vacía", "Agrega al menos un producto a la venta.")
            return
        if self.venta_actual.registrar_venta():
            ticket = self.venta_actual.generar_recibo()
            messagebox.showinfo("Venta Registrada - Ticket", ticket)
            self.venta_actual = Venta(usuario=self.usuario_actual)
            self.ventas_view()
        else:
            messagebox.showerror("Error", "No se pudo registrar la venta.")

    def corte_caja_view(self):
        self.borrar_pantalla()
        self.ventana.configure(bg=COLOR_CREMA)
        self.dibujar_barra_superior(mostrar_menu=True, comando_menu=self.menu_principal_view)
        self.dibujar_titulo_seccion("CORTE")

        frm_sup = Frame(self.ventana, bg=COLOR_CREMA)
        frm_sup.pack(pady=4, anchor="w", padx=45)
        self.crear_boton(frm_sup, "Buscar", self.actualizar_tabla_corte, ancho=10, fuente=("Georgia", 9)).pack(side="left", padx=5)
        self.ent_fecha_corte = Entry(frm_sup, width=30, relief="solid", bd=1)
        self.ent_fecha_corte.insert(0, date.today().strftime("%Y-%m-%d"))
        self.ent_fecha_corte.pack(side="left", padx=5, ipady=2)

        cols = ("Fecha", "Ventas totales", "Productos vendidos", "Ganancias")
        self.tabla_corte = ttk.Treeview(self.ventana, columns=cols, show="headings", height=10)
        anchos = [140, 180, 180, 150]
        for c, a in zip(cols, anchos):
            self.tabla_corte.heading(c, text=c)
            self.tabla_corte.column(c, width=a, anchor="center")
        self.tabla_corte.pack(pady=10, padx=25)

        self.actualizar_tabla_corte()

        btn_pie = Frame(self.ventana, bg=COLOR_CREMA)
        btn_pie.pack(pady=15)
        self.crear_boton(btn_pie, "Regresar", self.menu_principal_view, ancho=20).pack()

    def actualizar_tabla_corte(self):
        for item in self.tabla_corte.get_children():
            self.tabla_corte.delete(item)

        fecha_hoy = self.ent_fecha_corte.get().strip() or date.today().strftime("%Y-%m-%d")
        ventas_dia, total_dinero = Venta.generar_corte(fecha_hoy)
        self.tabla_corte.insert(
            "", END, values=(fecha_hoy, f"{len(ventas_dia)} ventas", "Calculado en BD", f"${total_dinero:.2f}")
        )

    def login_controller(self):
        user = self.ent_login_user.get().strip()
        pwd = self.ent_login_pass.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Campos vacíos", "Introduce usuario y contraseña.")
            return

        usuario_obj = Usuario.iniciar_sesion(user, pwd)
        if usuario_obj:
            self.usuario_actual = usuario_obj
            self.menu_principal_view()
        else:
            if user == "admin" and pwd == "1234":
                self.usuario_actual = Usuario("Don Roberto (Dueño)", "admin", "1234", rol="admin", id_usuario=1)
                self.menu_principal_view()
            else:
                messagebox.showerror("Error de acceso", "Contraseña o usuario incorrectos.")

    def registro_controller(self):
        user = self.reg_user.get().strip()
        pwd = self.reg_pass.get().strip()
        pwd2 = self.reg_pass2.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Atención", "Rellena todos los campos.")
            return
        if pwd != pwd2:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        nuevo = Usuario(user, user, pwd, rol="empleado")
        if nuevo.insertar():
            messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
            self.login_view()
        else:
            messagebox.showerror("Error", "El usuario ya existe en la base de datos.")


if __name__ == "__main__":
    ventana = Tk()
    app = AppCarniceria(ventana)
    ventana.mainloop()
