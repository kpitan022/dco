from tkinter import *
from tkinter import ttk
import sqlite3


class Encaython:
    db_name='database.db'
    def __init__(self,ventana):
        self.ventana=ventana
        ventana.title('Encaython')

        #------- creamos frame contenedor-
        contenedor=Frame(ventana)
        contenedor.pack(fill=BOTH,expand=1)
        #------- creamos canvas -------
        mi_canvas = Canvas(contenedor)
        mi_canvas.pack(side=LEFT,fill=BOTH,expand=1)

        # crea una barra de desplazamiento horizontal
        x_scroll = Scrollbar(ventana, orient=HORIZONTAL,command=mi_canvas.xview)
        # adjuntar barra de desplazamiento a la ventana raíz en
        x_scroll.pack(side=BOTTOM, fill=X)
        
        # crear una barra de desplazamiento vertical
        y_scroll = Scrollbar(contenedor, orient=VERTICAL,command=mi_canvas.yview)
        y_scroll.pack(side=RIGHT, fill=Y)

        mi_canvas.configure(yscrollcommand=y_scroll.set,xscrollcommand=x_scroll.set)

        mi_canvas.bind('<Configure>', lambda e: mi_canvas.configure(scrollregion= mi_canvas.bbox('all')))

        root= Frame(mi_canvas)

        # ---------- agregamos este ultimo frame al canvas
        mi_canvas.create_window((0,0), window=root,anchor='nw')


        #----------------aqui va el codigo (ejemplo de prueba)
        
        frame=LabelFrame(root, text='Cargar contenido')
        frame.grid(row=0, column=0,columnspan=3,pady=20,padx=20)
        # input titulo
        Label(frame,text='Titulo:').grid(row=1, column=0)
        self.e_titulo=Entry(frame)
        self.e_titulo.grid(row=1,column=1,sticky=W+E)
        self.e_titulo.focus()
        
        # input codigo
        Label(frame,text='Codigo:').grid(row=2, column=0)
        self.e_codigo=Text(frame)
        self.e_codigo.grid(row=2, column=1)

        Button(frame,text='Agregar').grid(row=4, columnspan=2,sticky=W+E)

        self.tabla=ttk.Treeview(frame,height=10,columns=1)
        self.tabla.grid(row=5, columnspan=2,sticky=W+E,padx=20)
        #creamos encabezado de la tabla
        # posicion celda del titulo, titulo de la columna, centrado de la columna 
        self.tabla.heading('#0',text='Instruccion', anchor=CENTER)

    def hacer_consluta(self,query,parametros=()):
        conn=sqlite3.connect(self.db_name)
        cursor=conn.cursor()
        resultado=cursor.execute(query,parametros)
        conn.commit()
        return resultado

if __name__ == '__main__':
    ventana = Tk()
    # instancio la clase Encaython y le paso como parametro la ventana(ventana)
    app = Encaython(ventana)
    ventana.mainloop()

