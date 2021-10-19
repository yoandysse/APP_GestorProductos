import time
import tkinter.ttk
from tkinter import *
from tkinter import ttk
import sqlite3
import db
from models import GestorProductos

class Producto:

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(0,0)
        self.ventana.wm_iconbitmap("recursos/icono.ico")

        self.contenedor_registrar_producto()
        self.contenedor_tabla_productos()
        self.contenedor_estadistica()
        self.f_get_productos()

        ############ Contenedor botonera ############
        # Botones de Editar y Eliminar
        boton_editar = ttk.Button(text="Editar", command=self.contenedor_edit_producto)
        boton_editar.grid(row=999, column=0, sticky=W + E, columnspan=2)

        boton_eliminar = ttk.Button(text="Eliminar", command=self.f_del_producto)
        boton_eliminar.grid(row=999, column=2, sticky=W + E, columnspan=2)



    def contenedor_registrar_producto(self):
        ############ Contenedor Registrar Producto ############
        registrar_producto = LabelFrame(self.ventana, text = "Registrar Producto")
        registrar_producto.grid(row = 0, column = 0)

        ## Label Nombre
        self.etiqueta_nombre = ttk.Label(registrar_producto, text="Nombre: ")
        self.etiqueta_nombre.grid(row = 0, column = 0)
        ## Entry Nombre
        self.nombre = ttk.Entry(registrar_producto)
        self.nombre.focus()
        self.nombre.grid(row = 0, column = 1)

        ## Label Categoria
        self.etiqueta_categoria = ttk.Label(registrar_producto, text="Categoria: ")
        self.etiqueta_categoria.grid(row = 1, column = 0)
        ## Entry Categoria
        self.categoria = ttk.Entry(registrar_producto)
        self.categoria.grid(row = 1, column = 1, sticky = W+E)

        ## Label Precio
        self.etiqueta_precio = ttk.Label(registrar_producto, text="Precio: ")
        self.etiqueta_precio.grid(row = 2, column = 0)
        ## Entry Precio
        self.precio = ttk.Entry(registrar_producto)
        self.precio.grid(row = 2, column = 1, sticky = W+E)

        ## Label Cantidad
        self.etiqueta_cantidad = ttk.Label(registrar_producto, text="Cantidad: ")
        self.etiqueta_cantidad.grid(row = 3, column = 0)
        ## Entry Cantidad
        self.cantidad = ttk.Entry(registrar_producto)
        self.cantidad.grid(row = 3, column = 1, sticky = W+E)

        ## Boton
        self.boton_guardar = ttk.Button(registrar_producto, text="Guardar \nProducto", command = self.f_add_producto)
        self.boton_guardar.grid(row = 0, column = 3, rowspan = 4, sticky = N+S)

        ## Mensaje de errore
        self.mensaje = ttk.Label(registrar_producto,text= '', anchor = CENTER, state="disabled")
        self.mensaje.grid(row = 4, columnspan = 4, sticky = W+E,)

    def contenedor_tabla_productos(self):
        ############ Contenedor Tabla de Productos ############
        tabla_productos = LabelFrame(self.ventana)
        tabla_productos.grid(row=1, column=0, columnspan=4, pady=10)

        # Estructura de la tabla
        self.tabla = ttk.Treeview(tabla_productos, column=("Categoria", "Precio", "Cantidad"))
        self.tabla.grid(row=6, column=0, columnspan=4)

        self.tabla.column("#0", width=150, minwidth=150)
        self.tabla.column("Categoria", width=150, minwidth=150)
        self.tabla.column("Precio", width=100, minwidth=100)
        self.tabla.column("Cantidad", width=80, minwidth=80)

        self.tabla.heading("#0", text="Nombre", anchor=CENTER)
        self.tabla.heading("Categoria", text="Categoria", anchor=CENTER)
        self.tabla.heading("Precio", text="Precio", anchor=CENTER)
        self.tabla.heading("Cantidad", text="Cantidad", anchor=CENTER)

    def contenedor_estadistica(self):
        ############ Contenedor Estadistica ############
        estadistica_productos = LabelFrame(self.ventana, text="Estadistica Productos")
        estadistica_productos.grid(row=0, column=2)

        ## Label Total de Productos
        self.total_productos = ttk.Label(estadistica_productos, text="Total de Productos: ")
        self.total_productos.grid(row=0, column=0)
        ## Label Valor Total de Productos
        self.valor_total_productos = ttk.Label(estadistica_productos, text="")
        self.valor_total_productos.grid(row=0, column=1)

        ## Label Cantidad de Productos
        self.cantidad_productos = ttk.Label(estadistica_productos, text="Cantidad de Productos: ")
        self.cantidad_productos.grid(row=1, column=0)
        ## Label Valor Cantidad de Productos
        self.valor_cantidad_productos = ttk.Label(estadistica_productos, text="")
        self.valor_cantidad_productos.grid(row=1, column=1)

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def f_get_productos(self):
        ### Borrar informacion de la tabla para pedir los datos de nuevo
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        registros = db.session.query(GestorProductos)
        cantidadProductos = 0

        ## Llenando Tabla
        for fila in registros:
            self.tabla.insert("",0, text= fila.nombre, values = (fila.categoria, fila.precio, fila.cantidad))
            cantidadProductos += int(fila.cantidad)

        ## Mostrando Estadistica
        self.valor_total_productos["text"] = str(registros.count())
        self.valor_cantidad_productos["text"] = cantidadProductos

    def validadion_nombre(self):
        nombre_introducido = self.nombre.get()

        if len(nombre_introducido) == 0:
            # print("CAMPO NOMBRE VACIO")
            return "El campo nombre no puede estar vacío"

        else:
            query = "SELECT nombre FROM producto WHERE nombre = ?"
            result = self.db_consulta(query, (nombre_introducido,))
            if result.fetchone() == None:
                return True
            else:
                # print("El nombre del producto ya existe")
                return "El nombre del producto ya existe"

    def validadion_categoria(self):
        categoria_introducido = self.categoria.get()

        if len(categoria_introducido) == 0:
            # print("CAMPO CATEGORIA VACIO")
            return "El campo categoria no puede estar vacío"
        else:
            return True

    def validadion_precio(self):
        precio_introducido = self.precio.get()

        if len(precio_introducido) == 0:
            return "El campo precio no puede estar vacío"
        else:
            return True

    def validadion_cantidad(self):
        cantidad_introducido = self.cantidad.get()
        if len(cantidad_introducido) == 0:
            # print("CAMPO CANTIDAD VACIO")
            return "El campo cantidad no puede estar vacío"
        else:
            return True

    def f_add_producto(self):
        if (self.validadion_nombre() and self.validadion_categoria() and self.validadion_precio() and self.validadion_cantidad()) == True:

            producto = GestorProductos(self.nombre.get(), self.categoria.get(),self.precio.get(), self.cantidad.get())
            db.session.add(producto)
            db.session.commit()


            self.mensaje["text"] = "Producto {} agregado correctamente".format(self.nombre.get())
            self.mensaje["foreground"] = "green"

            self.nombre.delete(0, END)
            self.categoria.delete(0, END)
            self.precio.delete(0, END)
            self.cantidad.delete(0, END)

            # Para debug
            # print("Datos Guardados")
            # print(self.nombre.get())
            # print(self.categoria.get())
            # print(self.precio.get())
            # print(self.cantidad.get())

        elif self.validadion_nombre() != True :
            self.mensaje["text"] = self.validadion_nombre()
            self.mensaje["foreground"] = "red"

        elif self.validadion_categoria() != True :
            self.mensaje["text"] = self.validadion_categoria()
            self.mensaje["foreground"] = "red"

        elif self.validadion_precio() != True :
            self.mensaje["text"] = self.validadion_precio()
            self.mensaje["foreground"] = "red"

        elif self.validadion_cantidad() != True :
            self.mensaje["text"] = self.validadion_cantidad()
            self.mensaje["foreground"] = "red"


        self.f_get_productos()

    def f_upd_producto(self):
        upd_producto = db.session.query(GestorProductos).filter_by(nombre=self.nombre.get()).first()

        upd_producto.nombre = self.nombre.get()
        upd_producto.categoria = self.categoria.get()
        upd_producto.precio = self.precio.get()
        upd_producto.cantidad = self.cantidad.get()

        db.session.commit()

        self.mensaje["text"] = "Producto {} editado correctamente".format(self.nombre.get())
        self.mensaje["foreground"] = "green"

        self.contenedor_registrar_producto()
        self.f_get_productos()


    def f_del_producto(self):
        # print(self.tabla.item(self.tabla.selection())) # Para debug
        nombre = self.tabla.item(self.tabla.selection())["text"]

        db.session.query(GestorProductos).filter_by(nombre=nombre).delete()
        db.session.commit()


        self.mensaje["text"] = "Producto {} eliminado correctamente".format(nombre)
        self.mensaje["foreground"] = "red"

        self.contenedor_registrar_producto()
        self.f_get_productos()

    def contenedor_edit_producto(self):
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Seleccione un producto antes editar"
            self.mensaje["foreground"] = "red"
            return

        nombre = self.tabla.item(self.tabla.selection())["text"]

        producto = db.session.query(GestorProductos).filter_by(nombre=nombre).first()
        # print(producto)

        ############ Contenedor Editar Producto ############
        editar_producto = LabelFrame(self.ventana, text="Editar Producto")
        editar_producto.grid(row=0, column=0)

        ## Label Nombre
        self.etiqueta_nombre = ttk.Label(editar_producto, text="Nombre: ")
        self.etiqueta_nombre.grid(row=0, column=0)
        ## Entry Nombre
        self.nombre = ttk.Entry(editar_producto)
        self.nombre.insert(0, producto.nombre)
        self.nombre.focus()
        self.nombre.grid(row=0, column=1)

        ## Label Categoria
        self.etiqueta_categoria = ttk.Label(editar_producto, text="Categoria: ")
        self.etiqueta_categoria.grid(row=1, column=0)
        ## Entry Categoria
        self.categoria = ttk.Entry(editar_producto)

        if producto.categoria == None:
            pass
        else:
            self.categoria.insert(0, producto.categoria)

        self.categoria.grid(row=1, column=1, sticky=W + E)

        ## Label Precio
        self.etiqueta_precio = ttk.Label(editar_producto, text="Precio: ")
        self.etiqueta_precio.grid(row=2, column=0)
        ## Entry Precio
        self.precio = ttk.Entry(editar_producto)
        self.precio.insert(0, producto.precio)
        self.precio.grid(row=2, column=1, sticky=W + E)

        ## Label Cantidad
        self.etiqueta_cantidad = ttk.Label(editar_producto, text="Cantidad: ")
        self.etiqueta_cantidad.grid(row=3, column=0)
        # Entry Cantidad
        self.cantidad = ttk.Entry(editar_producto)
        self.cantidad.insert(0, producto.cantidad)
        self.cantidad.grid(row=3, column=1, sticky=W + E)

        ## Boton
        self.boton_guardar = ttk.Button(editar_producto, text="Actualizar \nProducto", command=self.f_upd_producto)
        self.boton_guardar.grid(row=0, column=3, rowspan=2, sticky=N + S)
        self.boton_guardar = ttk.Button(editar_producto, text="Eliminar \nProducto", command=self.f_del_producto)
        self.boton_guardar.grid(row=2, column=3, rowspan=2, sticky=N + S)

        ## Mensaje de errore
        self.mensaje = ttk.Label(editar_producto, text='', anchor=CENTER, state="disabled")
        self.mensaje.grid(row=4, columnspan=4, sticky=W + E, )


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)

    root = Tk() # Instancia de la ventana principal
    app = Producto(root)
    root.mainloop()

