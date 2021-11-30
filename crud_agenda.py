from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from tkinter import messagebox
import mysql.connector
import re


root = Tk()
root.title("CRUD Agenda UTN")
root.geometry("720x500")
root.configure(bg="#262626")


# Botones y campos de entrada
operaciones = LabelFrame(root, text="Alta, Baja, Modificación y Consulta",
foreground="white")
operaciones.pack(fill="both", expand=True, padx=10, pady=5, anchor=CENTER)
operaciones.config(highlightcolor="white", bg="#262626", highlightthickness=2,
relief="flat")


# Campos de entrada
nombre_label = Label(operaciones, text="Nombre", bg="#262626",
foreground="white")
nombre_label.grid(row=0, column=0, padx=10, pady=10)
nombre_entry = Entry(operaciones, foreground="#C00000", font=BOLD)
nombre_entry.grid(row=0, column=1, padx=10, pady=10)

apellido_label = Label(operaciones, text="Apellido", bg="#262626",
foreground="white")
apellido_label.grid(row=1, column=0, padx=10, pady=10)
apellido_entry = Entry(operaciones, foreground="#C00000", font=BOLD)
apellido_entry.grid(row=1, column=1, padx=10, pady=10)

telefono_label = Label(operaciones, text="Teléfono", bg="#262626",
foreground="white")
telefono_label.grid(row=0, column=2, padx=10, pady=10)
telefono_entry = Entry(operaciones, foreground="#C00000", font=BOLD)
telefono_entry.grid(row=0, column=3, padx=10, pady=10)

id_label = Label(operaciones, text="ID", bg="#262626",
foreground="white")
id_label.grid(row=1, column=2, padx=10, pady=10)
id_entry = Entry(operaciones, foreground="#C00000", font=BOLD)
id_entry.grid(row=1, column=3, padx=10, pady=10)


# Funciones
def crear_bd():
    mibase = mysql.connector.connect(host = "localhost", user = "root",
    passwd = "")
    micursor = mibase.cursor()
    micursor.execute("CREATE DATABASE IF NOT EXISTS agenda_crud")
    mibase.close()
    
    mibase = mysql.connector.connect(host = "localhost", user = "root",
    passwd = "", database = "agenda_crud")
    micursor = mibase.cursor()
    micursor.execute("""
    CREATE TABLE IF NOT EXISTS agenda 
    (id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre varchar(128) COLLATE utf8_spanish2_ci NOT NULL,
    apellido varchar(128) COLLATE utf8_spanish2_ci NOT NULL,
    telefono varchar(128) COLLATE utf8_spanish2_ci NOT NULL)""")
    mibase.close()

crear_bd()

def borrar_campos():
    nombre_entry.delete(0, END)
    apellido_entry.delete(0, END)
    telefono_entry.delete(0, END)
    id_entry.delete(0, END)


def rellenar_campos():
    nombre_entry.delete(0, END)
    apellido_entry.delete(0, END)
    telefono_entry.delete(0, END)
    
    agenda = mysql.connector.connect(host = "localhost",
    user = "root", passwd = "", database = "agenda_crud")

    micursor = agenda.cursor()

    sql = "SELECT * FROM agenda WHERE id = %s"
    datos = (id_entry.get(),)

    micursor.execute(sql, datos)

    resultado = micursor.fetchone()

    nombre_entry.insert(0, resultado[1])
    apellido_entry.insert(0, resultado[2])
    telefono_entry.insert(0, resultado[3])
    agenda.close()



def click(e):
    borrar_campos()

    selected = tree.focus()
    values = tree.item(selected, 'values')

    nombre_entry.insert(0, values[1])
    apellido_entry.insert(0, values[2])
    telefono_entry.insert(0, values[3])
    id_entry.insert(0, values[0])


def alta_registro():
    cadena1 = nombre_entry.get()
    cadena2 = apellido_entry.get()
    cadena3 = telefono_entry.get()
    patron = "^[a-zA-Z áéíóúü]{3,26}$"
    patron2 = "^[0-9 ]{6,26}$"
    
    if not (re.match(patron, cadena1)):
        messagebox.showerror(message="""
El nombre sólo puede contener letras.
(entre 3 y 25 caracteres de longitud)""", title="ADVERTENCIA!")

    elif not (re.match(patron, cadena2)):
        messagebox.showerror(message="""
El apellido sólo puede contener letras.
(entre 3 y 25 caracteres de longitud)""", title="ADVERTENCIA!")
    
    elif not (re.match(patron2, cadena3)):
        messagebox.showerror(message="""
El teléfono sólo puede contener números.
(entre 6 y 25 caracteres de longitud)""", title="ADVERTENCIA!")

    else:
        agenda = mysql.connector.connect(host = "localhost",
        user = "root", passwd = "", database = "agenda_crud")

        micursor = agenda.cursor()

        sql = """INSERT INTO agenda (nombre, apellido, telefono)
        VALUES (%s, %s, %s)"""
        datos = (nombre_entry.get(), apellido_entry.get(), telefono_entry.get())

        micursor.execute(sql, datos)

        agenda.commit()

        messagebox.showinfo(message="Registro agregado con éxito.",
        title="Éxito!")
        agenda.close()


def baja_registro():
    baja_pregunta = messagebox.askyesno(message="""
El registro será borrado.
¿Desea continuar?""", title="ADVERTENCIA!")

    if baja_pregunta == True:

        agenda = mysql.connector.connect(host = "localhost",
        user = "root", passwd = "", database = "agenda_crud")

        micursor = agenda.cursor()

        sql = "DELETE FROM agenda WHERE id = %s"
        datos = (id_entry.get(),)

        micursor.execute(sql, datos)

        agenda.commit()

        messagebox.showinfo(message="Registro borrado con éxito.",
            title="Éxito!")
        agenda.close()


def consultar_registros():
    for i in tree.get_children():
        tree.delete(i)

    agenda = mysql.connector.connect(host = "localhost",
    user = "root", passwd = "", database = "agenda_crud")

    micursor = agenda.cursor()

    sql = "SELECT * FROM agenda"

    micursor.execute(sql)

    resultado = micursor.fetchall()
    
    tree.tag_configure("oddrow", background="grey", foreground="white")
    tree.tag_configure("evenrow", background="lightgrey")

    global contador
    contador = 0

    for x in resultado:
        
        if contador % 2 == 0:
            tree.insert(
                parent="",
                index="end",
                iid=contador,
                text="",
                values=x,
                tags=("evenrow",))
        else:
            tree.insert(
                parent="",
                index="end",
                iid=contador,
                text="",
                values=x,
                tags=("oddrow",))
        
        contador += 1
    agenda.close()


def buscar_registro():
    for i in tree.get_children():
        tree.delete(i)

    agenda = mysql.connector.connect(host = "localhost",
    user = "root", passwd = "", database = "agenda_crud")

    micursor = agenda.cursor()

    sql = "SELECT * FROM agenda WHERE id = %s"
    datos = (id_entry.get(),)

    micursor.execute(sql, datos)

    resultado = micursor.fetchone()
    
    tree.tag_configure("evenrow", background="grey")

    tree.insert(
                parent="",
                index="end",
                text="",
                values=resultado,
                tags=("evenrow",))
    
    agenda.close()


def modificar_registro():
    modificacion_pregunta = messagebox.askyesno(message="""
El registro será modificado.
¿Desea continuar?""", title="ADVERTENCIA!")

    if modificacion_pregunta == True:
        cadena1 = nombre_entry.get()
        cadena2 = apellido_entry.get()
        cadena3 = telefono_entry.get()
        patron = "^[a-zA-Z áéíóúü]{3,26}$"
        patron2 = "^[0-9 ]{6,26}$"
        
        if not (re.match(patron, cadena1)):
            messagebox.showerror(message="""
    El nombre sólo puede contener letras.
    (entre 3 y 25 caracteres de longitud)""", title="ADVERTENCIA!")

        elif not (re.match(patron, cadena2)):
            messagebox.showerror(message="""
    El apellido sólo puede contener letras.
    (entre 3 y 25 caracteres de longitud)""", title="ADVERTENCIA!")
        
        elif not (re.match(patron2, cadena3)):
            messagebox.showerror(message="""
    El teléfono sólo puede contener números.
    (entre 6 y 25 caracteres de longitud)""", title="ADVERTENCIA!")

        else:
            agenda = mysql.connector.connect(host = "localhost",
            user = "root", passwd = "", database = "agenda_crud")

            micursor = agenda.cursor()

            sql = """UPDATE agenda SET nombre = %s, apellido = %s, telefono =%s
            WHERE id = %s"""

            datos = (nombre_entry.get(),
                    apellido_entry.get(),
                    telefono_entry.get(),
                    id_entry.get())

            micursor.execute(sql, datos)

            agenda.commit()

            messagebox.showinfo(message="Registro modificado con éxito.",
            title="Éxito!")
            agenda.close()



# Botones Alta, Baja, Modificación y Consulta
alta_button = Button(operaciones, text="Alta",bg="white",
activebackground="green",activeforeground="white",
command=lambda:[alta_registro(), borrar_campos(),
consultar_registros()])
alta_button.grid(row=3, column=0, padx=10, pady=10)

baja_button = Button(operaciones, text="Baja", bg="white",
activebackground="red",activeforeground="white",
command=lambda:[baja_registro(), borrar_campos(), consultar_registros()])
baja_button.grid(row=3, column=1, padx=10, pady=10)

modificacion_button = Button(operaciones, text="Modificación", bg="white",
activebackground="#E58900",activeforeground="white",
command=lambda:[modificar_registro(), borrar_campos(), consultar_registros()])
modificacion_button.grid(row=3, column=2, padx=10, pady=10)

busqueda_button = Button(operaciones, text="Búsqueda por ID", bg="white",
activebackground="blue",activeforeground="white",
command=lambda:[buscar_registro(), rellenar_campos()])
busqueda_button.grid(row=3, column=3, padx=10, pady=10)

borrar_campos_button = Button(operaciones, text="Borrar campos", bg="white",
activebackground="#7000A8",activeforeground="white", command=borrar_campos)
borrar_campos_button.grid(row=4, column=1, padx=10, pady=10)

mostrar_tabla_button = Button(operaciones, text="Mostrar tabla",
bg="white", activebackground="#C60070",activeforeground="white",
command=lambda:[borrar_campos(), consultar_registros()])
mostrar_tabla_button.grid(row=4, column=2, padx=10, pady=10)


# Visualización de datos en agenda

# Treeview
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3")
style.map("Treeview",
    background=[("selected", "red")])

tree_frame = Frame(root)
tree_frame.pack(fill="both", expand=True, padx=10, pady=10, anchor=CENTER)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,
selectmode="extended")
tree.pack()

tree_scroll.configure(command=tree.yview)

tree["columns"] = ("ID", "Nombre", "Apellido", "Teléfono")
tree.column("#0", width=0, stretch=NO)
tree.column("ID", anchor=W, width=80)
tree.column("Nombre", anchor=W, width=230)
tree.column("Apellido", anchor=W, width=230)
tree.column("Teléfono", anchor=W, width=230)

tree.heading("#0", text="", anchor=W)
tree.heading("ID", text="ID", anchor=W)
tree.heading("Nombre", text="Nombre", anchor=W)
tree.heading("Apellido", text="Apellido", anchor=W)
tree.heading("Teléfono", text="Teléfono", anchor=W)

tree.bind("<ButtonRelease-1>", click)

mainloop()
