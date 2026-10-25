"""
UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
Curso: Programación (Código: 213023) - Fase 3
Ejercicio 4: Sistema de Tienda Virtual (Virtual Store System)
Marco Steven Rodríguez Montoya
Temáticas: Herencia, Polimorfismo, Sobrecarga y GUI con Panel Lateral de Inventario.
"""

import tkinter as tk
from tkinter import ttk, messagebox
# 1. MODELO ORIENTADO A OBJETOS: CLASE BASE Y SUBCLASES
class Producto:
    """Clase base que modela los atributos y métodos comunes de un producto."""
    def __init__(self, nombre: str, precio: float, stock: int):
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)

    def descripcion(self) -> str:
        """Método polimórfico base para describir el producto."""
        return f"{self.nombre} (Stock: {self.stock})"

    def obtener_atributo_especial(self) -> str:
        """Retorna el atributo diferenciador de la subclase."""
        return "N/A"

    def calcular_descuento(self, porcentaje: float = 0.0, cupon: str = None, cliente_premium: bool = False) -> float:
        """
        Sobrecarga simulada mediante argumentos por defecto:
        1. calcular_descuento(porcentaje)
        2. calcular_descuento(porcentaje, cupon)
        3. calcular_descuento(porcentaje, cupon, cliente_premium)
        """
        descuento_unitario = self.precio * (porcentaje / 100.0)

        if cupon and cupon.strip().upper() == "PROMO5":
            descuento_unitario += self.precio * 0.05

        if cliente_premium:
            descuento_unitario += self.precio * 0.10

        return min(descuento_unitario, self.precio)

    def calcular_precio_final(self, porcentaje: float = 0.0, cupon: str = None, cliente_premium: bool = False) -> float:
        """Calcula el valor neto unitario tras descontar las promociones aplicables."""
        rebaja = self.calcular_descuento(porcentaje, cupon, cliente_premium)
        return max(0.0, self.precio - rebaja)


class ProductoElectronico(Producto):
    """Subclase para tecnología con depreciación acelerada."""
    def __init__(self, nombre: str, precio: float, stock: int, meses_garantia: int = 12):
        super().__init__(nombre, precio, stock)
        self.meses_garantia = meses_garantia

    def descripcion(self) -> str:
        return f"[Electronics] {self.nombre} | Warranty: {self.meses_garantia} mo"

    def obtener_atributo_especial(self) -> str:
        return f"{self.meses_garantia} Months"

    def calcular_descuento(self, porcentaje: float = 0.0, cupon: str = None, cliente_premium: bool = False) -> float:
        rebaja_base = super().calcular_descuento(porcentaje, cupon, cliente_premium)
        depreciacion = self.precio * 0.08
        return min(self.precio, rebaja_base + depreciacion)


class ProductoAlimento(Producto):
    """Subclase para alimentos perecederos con tope máximo de rebaja."""
    def __init__(self, nombre: str, precio: float, stock: int, fecha_vencimiento: str = "2026-12-31"):
        super().__init__(nombre, precio, stock)
        self.fecha_vencimiento = fecha_vencimiento

    def descripcion(self) -> str:
        return f"[Food] {self.nombre} | Exp: {self.fecha_vencimiento}"

    def obtener_atributo_especial(self) -> str:
        return self.fecha_vencimiento

    def calcular_descuento(self, porcentaje: float = 0.0, cupon: str = None, cliente_premium: bool = False) -> float:
        rebaja_calculada = super().calcular_descuento(porcentaje, cupon, cliente_premium)
        tope_maximo = self.precio * 0.25
        return min(rebaja_calculada, tope_maximo)


class ProductoRopa(Producto):
    """Subclase para vestuario con descuentos acumulables por temporada."""
    def __init__(self, nombre: str, precio: float, stock: int, talla: str = "M"):
        super().__init__(nombre, precio, stock)
        self.talla = talla

    def descripcion(self) -> str:
        return f"[Clothing] {self.nombre} | Size: {self.talla}"

    def obtener_atributo_especial(self) -> str:
        return f"Size {self.talla}"

    def calcular_descuento(self, porcentaje: float = 0.0, cupon: str = None, cliente_premium: bool = False) -> float:
        rebaja_estandar = super().calcular_descuento(porcentaje, cupon, cliente_premium)
        bonus_temporada = self.precio * 0.12
        return min(self.precio, rebaja_estandar + bonus_temporada)

# 2. GESTOR POLIMÓRFICO: CarritoDeCompras
class CarritoDeCompras:
    """Gestiona los productos agregados a la orden de compra y sus cantidades."""
    def __init__(self):
        self.items = []

    def agregar_producto(self, producto: Producto, cantidad: int):
        self.items.append((producto, cantidad))

    def vaciar(self):
        self.items.clear()

    def calcular_totales(self, porcentaje: float = 0.0, cupon: str = None, cliente_premium: bool = False) -> tuple:
        subtotal_gen = 0.0
        descuento_gen = 0.0
        total_pagar = 0.0

        for prod, qty in self.items:
            subtotal_item = prod.precio * qty
            descuento_item = prod.calcular_descuento(porcentaje, cupon, cliente_premium) * qty
            neto_item = prod.calcular_precio_final(porcentaje, cupon, cliente_premium) * qty

            subtotal_gen += subtotal_item
            descuento_gen += descuento_item
            total_pagar += neto_item

        return subtotal_gen, descuento_gen, total_pagar

# 3. INTERFAZ GRÁFICA TKINTER CON LAYOUT LATERAL (INVENTARIO VS COMPRAS)
class VirtualStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce Virtual Store - UNAD Phase 3")
        self.root.geometry("1240x720")
        self.root.minsize(1100, 650)

        # Inicia con inventario vacío
        self.inventario_almacen = []
        self.carrito = CarritoDeCompras()

        self.setup_ui()

    def setup_ui(self):
        # Contenedor principal dividido en dos columnas
        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(fill="both", expand=True)

        # BLOQUE LATERAL IZQUIERDO: WAREHOUSE & INVENTORY
        frame_sidebar = ttk.LabelFrame(main_container, text=" Warehouse Inventory (Back-Office) ", padding=10)
        frame_sidebar.pack(side="left", fill="both", expand=False, padx=(0, 10))

        # Sub-marco: Formulario de alta
        frame_admin_form = ttk.Frame(frame_sidebar)
        frame_admin_form.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_admin_form, text="Category:").grid(row=0, column=0, sticky="w", pady=2)
        self.combo_cat = ttk.Combobox(frame_admin_form, values=["Electronics", "Food", "Clothing"], state="readonly", width=14)
        self.combo_cat.set("Electronics")
        self.combo_cat.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        self.combo_cat.bind("<<ComboboxSelected>>", self.on_category_change)

        ttk.Label(frame_admin_form, text="Product Name:").grid(row=1, column=0, sticky="w", pady=2)
        self.txt_admin_name = ttk.Entry(frame_admin_form, width=16)
        self.txt_admin_name.grid(row=1, column=1, sticky="ew", pady=2, padx=5)

        ttk.Label(frame_admin_form, text="Base Price ($):").grid(row=2, column=0, sticky="w", pady=2)
        self.txt_admin_price = ttk.Entry(frame_admin_form, width=16)
        self.txt_admin_price.grid(row=2, column=1, sticky="ew", pady=2, padx=5)

        ttk.Label(frame_admin_form, text="Initial Stock:").grid(row=3, column=0, sticky="w", pady=2)
        self.txt_admin_stock = ttk.Entry(frame_admin_form, width=16)
        self.txt_admin_stock.grid(row=3, column=1, sticky="ew", pady=2, padx=5)

        self.lbl_admin_extra = ttk.Label(frame_admin_form, text="Warranty (Mo):")
        self.lbl_admin_extra.grid(row=4, column=0, sticky="w", pady=2)
        self.txt_admin_extra = ttk.Entry(frame_admin_form, width=16)
        self.txt_admin_extra.insert(0, "12")
        self.txt_admin_extra.grid(row=4, column=1, sticky="ew", pady=2, padx=5)

        btn_save = ttk.Button(frame_admin_form, text="Add to Warehouse Stock", command=self.registrar_producto_bodega)
        btn_save.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(8, 4))

        # Sub-marco: Tabla de stock lateral
        ttk.Label(frame_sidebar, text="Current Stock by Category:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 2))

        stock_cols = ("Category", "Item", "Qty", "Attribute", "Price")
        self.tree_stock = ttk.Treeview(frame_sidebar, columns=stock_cols, show="headings", height=16)

        self.tree_stock.heading("Category", text="Category")
        self.tree_stock.column("Category", width=85, anchor="center")

        self.tree_stock.heading("Item", text="Item")
        self.tree_stock.column("Item", width=120, anchor="w")

        self.tree_stock.heading("Qty", text="Qty")
        self.tree_stock.column("Qty", width=45, anchor="center")

        self.tree_stock.heading("Attribute", text="Size/Exp/Warr")
        self.tree_stock.column("Attribute", width=105, anchor="center")

        self.tree_stock.heading("Price", text="Price")
        self.tree_stock.column("Price", width=75, anchor="center")

        self.tree_stock.pack(fill="both", expand=True)

        # BLOQUE DERECHO: STORE, CART & CHECKOUT
        frame_main = ttk.Frame(main_container)
        frame_main.pack(side="right", fill="both", expand=True)

        # Panel Superior de Compra
        frame_shop = ttk.LabelFrame(frame_main, text=" Store Front & Discounts ", padding=10)
        frame_shop.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_shop, text="Select Item:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.combo_customer_prod = ttk.Combobox(frame_shop, state="readonly", width=28)
        self.combo_customer_prod.grid(row=0, column=1, sticky="w", padx=5, pady=4)
        self.combo_customer_prod.bind("<<ComboboxSelected>>", self.on_warehouse_product_selected)

        ttk.Label(frame_shop, text="Qty:").grid(row=0, column=2, sticky="e", padx=5, pady=4)
        self.txt_customer_qty = ttk.Entry(frame_shop, width=6)
        self.txt_customer_qty.insert(0, "1")
        self.txt_customer_qty.grid(row=0, column=3, sticky="w", padx=5, pady=4)

        btn_add = ttk.Button(frame_shop, text="Add to Cart", command=self.agregar_al_carrito)
        btn_add.grid(row=0, column=4, padx=10, pady=4)

        self.lbl_selected_info = ttk.Label(frame_shop, text="Available Stock: - | Unit Price: -", font=("Arial", 9, "italic"))
        self.lbl_selected_info.grid(row=0, column=5, sticky="w", padx=10, pady=4)

        # Configuración de sobrecarga
        ttk.Label(frame_shop, text="Base Discount (%):").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.txt_disc_pct = ttk.Entry(frame_shop, width=10)
        self.txt_disc_pct.insert(0, "10")
        self.txt_disc_pct.grid(row=1, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(frame_shop, text="Coupon:").grid(row=1, column=2, sticky="e", padx=5, pady=4)
        self.txt_coupon = ttk.Entry(frame_shop, width=10)
        self.txt_coupon.insert(0, "PROMO5")
        self.txt_coupon.grid(row=1, column=3, sticky="w", padx=5, pady=4)

        self.chk_premium_var = tk.BooleanVar(value=True)
        self.chk_premium = ttk.Checkbutton(frame_shop, text="VIP / Premium Client Status", variable=self.chk_premium_var)
        self.chk_premium.grid(row=1, column=4, columnspan=2, sticky="w", padx=10, pady=4)

        # Panel del Carrito
        frame_cart = ttk.LabelFrame(frame_main, text=" Shopping Cart (Polymorphic Review) ", padding=10)
        frame_cart.pack(fill="both", expand=True)

        cart_cols = ("Item", "Category", "Description", "Unit Price", "Qty", "Subtotal", "Total Discount", "Final Total")
        self.tree_cart = ttk.Treeview(frame_cart, columns=cart_cols, show="headings", height=12)

        self.tree_cart.heading("Item", text="#")
        self.tree_cart.column("Item", width=35, anchor="center")

        self.tree_cart.heading("Category", text="Category")
        self.tree_cart.column("Category", width=85, anchor="center")

        self.tree_cart.heading("Description", text="Description")
        self.tree_cart.column("Description", width=220, anchor="w")

        self.tree_cart.heading("Unit Price", text="Unit Price")
        self.tree_cart.column("Unit Price", width=85, anchor="center")

        self.tree_cart.heading("Qty", text="Qty")
        self.tree_cart.column("Qty", width=50, anchor="center")

        self.tree_cart.heading("Subtotal", text="Subtotal")
        self.tree_cart.column("Subtotal", width=90, anchor="center")

        self.tree_cart.heading("Total Discount", text="Total Discount")
        self.tree_cart.column("Total Discount", width=100, anchor="center")

        self.tree_cart.heading("Final Total", text="Final Total")
        self.tree_cart.column("Final Total", width=100, anchor="center")

        self.tree_cart.pack(side="left", fill="both", expand=True)
        scrollbar_cart = ttk.Scrollbar(frame_cart, orient="vertical", command=self.tree_cart.yview)
        self.tree_cart.configure(yscrollcommand=scrollbar_cart.set)
        scrollbar_cart.pack(side="right", fill="y")

        # Barra inferior de totales
        frame_footer = ttk.Frame(frame_main, padding=10)
        frame_footer.pack(fill="x", pady=(10, 0))

        self.lbl_totals = ttk.Label(
            frame_footer,
            text="Items: 0 | Subtotal: $0.00 | Total Savings: $0.00 | Net Total: $0.00",
            font=("Arial", 10, "bold")
        )
        self.lbl_totals.pack(side="left")

        btn_clear = ttk.Button(frame_footer, text="Empty Cart", command=self.vaciar_carrito)
        btn_clear.pack(side="right", padx=5)

        btn_calc = ttk.Button(frame_footer, text="Recalculate & Apply Discounts", command=self.actualizar_vista_carrito)
        btn_calc.pack(side="right", padx=5)

    def on_category_change(self, event=None):
        cat = self.combo_cat.get()
        self.txt_admin_extra.delete(0, tk.END)
        if cat == "Electronics":
            self.lbl_admin_extra.config(text="Warranty (Mo):")
            self.txt_admin_extra.insert(0, "12")
        elif cat == "Food":
            self.lbl_admin_extra.config(text="Exp. Date:")
            self.txt_admin_extra.insert(0, "2026-12-31")
        elif cat == "Clothing":
            self.lbl_admin_extra.config(text="Size / Measure:")
            self.txt_admin_extra.insert(0, "L")

    def registrar_producto_bodega(self):
        cat = self.combo_cat.get()
        name = self.txt_admin_name.get().strip()
        price_str = self.txt_admin_price.get().strip()
        stock_str = self.txt_admin_stock.get().strip()
        extra = self.txt_admin_extra.get().strip()

        if not name or not price_str or not stock_str or not extra:
            messagebox.showwarning("Incomplete", "Please complete all fields.")
            return

        try:
            price = float(price_str)
            stock = int(stock_str)
            if price <= 0 or stock <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Price and Stock must be positive numbers.")
            return

        if cat == "Electronics":
            try:
                warranty = int(extra)
            except ValueError:
                warranty = 12
            p = ProductoElectronico(name, price, stock, warranty)
        elif cat == "Food":
            p = ProductoAlimento(name, price, stock, extra)
        else:
            p = ProductoRopa(name, price, stock, extra)

        self.inventario_almacen.append(p)
        self.actualizar_tabla_inventario_lateral()
        self.actualizar_combo_selector()

        self.txt_admin_name.delete(0, tk.END)
        self.txt_admin_price.delete(0, tk.END)
        self.txt_admin_stock.delete(0, tk.END)
        messagebox.showinfo("Success", f"{p.nombre} added to Warehouse inventory.")

    def actualizar_tabla_inventario_lateral(self):
        for row in self.tree_stock.get_children():
            self.tree_stock.delete(row)

        for p in self.inventario_almacen:
            cat_name = type(p).__name__.replace("Producto", "")
            self.tree_stock.insert("", "end", values=(
                cat_name,
                p.nombre,
                p.stock,
                p.obtener_atributo_especial(),
                f"${p.precio:.2f}"
            ))

    def actualizar_combo_selector(self):
        nombres = [f"[{type(p).__name__.replace('Producto','')}] {p.nombre}" for p in self.inventario_almacen]
        self.combo_customer_prod["values"] = nombres
        if nombres:
            self.combo_customer_prod.current(len(nombres) - 1)
            self.on_warehouse_product_selected()
        else:
            self.combo_customer_prod.set("")
            self.lbl_selected_info.config(text="Available Stock: - | Unit Price: -")

    def on_warehouse_product_selected(self, event=None):
        idx = self.combo_customer_prod.current()
        if 0 <= idx < len(self.inventario_almacen):
            p = self.inventario_almacen[idx]
            self.lbl_selected_info.config(text=f"Available Stock: {p.stock} | Unit Price: ${p.precio:.2f}")

    def agregar_al_carrito(self):
        idx = self.combo_customer_prod.current()
        if idx < 0 or idx >= len(self.inventario_almacen):
            messagebox.showwarning("Warning", "Select a product from the list.")
            return

        try:
            qty = int(self.txt_customer_qty.get().strip())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return

        prod = self.inventario_almacen[idx]
        if qty > prod.stock:
            messagebox.showerror("Error", f"Insufficient stock. Only {prod.stock} available.")
            return

        prod.stock -= qty
        self.carrito.agregar_producto(prod, qty)

        # Actualiza el inventario lateral y el carrito
        self.actualizar_tabla_inventario_lateral()
        self.on_warehouse_product_selected()
        self.actualizar_vista_carrito()

    def actualizar_vista_carrito(self):
        try:
            pct = float(self.txt_disc_pct.get().strip())
        except ValueError:
            pct = 0.0

        coupon = self.txt_coupon.get().strip()
        is_premium = self.chk_premium_var.get()

        for row in self.tree_cart.get_children():
            self.tree_cart.delete(row)

        for idx, (prod, qty) in enumerate(self.carrito.items, start=1):
            cat_name = type(prod).__name__.replace("Producto", "")
            desc = prod.descripcion()
            u_price = prod.precio
            subtotal = u_price * qty
            total_discount = prod.calcular_descuento(pct, coupon, is_premium) * qty
            final_total = prod.calcular_precio_final(pct, coupon, is_premium) * qty

            self.tree_cart.insert("", "end", values=(
                idx,
                cat_name,
                desc,
                f"${u_price:.2f}",
                qty,
                f"${subtotal:.2f}",
                f"${total_discount:.2f}",
                f"${final_total:.2f}"
            ))

        subt, tot_disc, final_tot = self.carrito.calcular_totales(pct, coupon, is_premium)
        self.lbl_totals.config(
            text=f"Items: {len(self.carrito.items)} | Subtotal: ${subt:.2f} | Total Savings: ${tot_disc:.2f} | Net Total: ${final_tot:.2f}"
        )

    def vaciar_carrito(self):
        if not self.carrito.items:
            return
        if messagebox.askyesno("Confirm", "Empty the shopping cart? Stock will be restored to Warehouse."):
            for prod, qty in self.carrito.items:
                prod.stock += qty
            self.carrito.vaciar()
            self.actualizar_tabla_inventario_lateral()
            self.on_warehouse_product_selected()
            self.actualizar_vista_carrito()

# 4. PUNTO DE ENTRADA PRINCIPAL
if __name__ == "__main__":
    root_window = tk.Tk()
    app = VirtualStoreApp(root_window)
    root_window.mainloop()