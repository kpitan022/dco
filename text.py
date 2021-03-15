from tkinter import *
from tkinter import ttk
import sqlite3

class Encaython:
    db_name='database.db'

    def __init__(self,ventana):
        self.ventana=ventana
        ventana.title('Encaython')

        #------- creamos self.frame contenedor-
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

        self.root= Frame(mi_canvas)

        # ---------- agregamos este ultimo self.frame al canvas
        mi_canvas.create_window((0,0), window=self.root,anchor='nw')

        #----------------aqui va el codigo (ejemplo de prueba)
        #  ventana cargar contenido
        Button(self.root,text='Agregar Contenido',command=self.menu_contenido).grid(row=0, column=0,pady=5)
        

    def menu_contenido(self):
        self.frame=LabelFrame(self.root, text='Cargar contenido')
        self.frame.grid(row=1, column=0,columnspan=3,pady=20,padx=20)
        # input titulo
        Label(self.frame,text='Titulo:').grid(row=0, column=0)
        self.e_titulo=Entry(self.frame)
        self.e_titulo.grid(row=0,column=1,sticky=W+E)
        self.e_titulo.focus()
        
        # input codigo
        Label(self.frame,text='Codigo:').grid(row=1, column=0)
        self.e_codigo=Text(self.frame)
        self.e_codigo.grid(row=1, column=1)

                # input codigo
        Label(self.frame,text='Resultado:').grid(row=2, column=0)
        self.e_resultado=Text(self.frame)
        self.e_resultado.grid(row=2, column=1)

        Button(self.frame,text='Agregar',command=self.agregar_contenido).grid(row=4, columnspan=2,pady=5,sticky=W+E)

        # mensajes
        self.mensaje=Label(self.frame,text='',fg='red',anchor=CENTER)
        self.mensaje.grid(row=100,column=0,sticky=W+E,columnspan=2)

        #    ventana ver contenido
        self.listbox = Listbox(self.frame)
        self.listbox.grid(row=1,column=3,rowspan=2,sticky=W+E+N+S,padx=20)


        self.crea_tabla()
        self.obtener_titulos()

    def hacer_consluta(self,query,parametros=()):
        conn=sqlite3.connect(self.db_name)
        cursor=conn.cursor()
        resultado=cursor.execute(query,parametros)
        conn.commit()
        return resultado

    def crea_tabla(self):
        query='''
        CREATE TABLE IF NOT EXISTS "sql" (
            "id"	INTEGER NOT NULL,
            "titulo"	TEXT,
            "codigo"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        )'''
        tabla_db=self.hacer_consluta(query)
        return tabla_db

    def obtener_titulos(self):
        self.boxing=[]
        self.listbox.get(0, END)
        self.listbox.delete(0,END)
        query='SELECT *FROM sql ORDER BY titulo'
        # llamo a la funcion hacer consulta y le paso el parametro
        filas_db=self.hacer_consluta(query)
        # recorro los datos devueltos por la consulta y los recorro para agregarlos a la tabla
        for fila in filas_db:
            self.boxing.append(fila[1])
        self.listbox.insert(0, *self.boxing)
        return self.boxing

    # TODO hacer funcion para validar form minuto 53
    
    def agregar_contenido(self):
        #genero la query
        query= 'INSERT INTO sql VALUES(NULL,?,?)'
        parametros=(self.e_titulo.get(),self.e_codigo.get(1.0,END))
        self.hacer_consluta(query,parametros)
        self.obtener_titulos()
        self.mensaje['text']=f'El contenido {self.e_titulo.get()} fue agregado correctamente'
        #borramos contenido de los entrys
        self.e_titulo.delete(0,END)
        #TODO borrar el contenido del text
        self.e_codigo.delete(1.0,END)

    def listar_tablas(self):
        query=f'''SELECT * FROM sqlite_master WHERE type = "table"'''
        lista_tablas=self.hacer_consluta(query)
        for lista in lista_tablas:
            print(lista)

if __name__ == '__main__':
    ventana = Tk()
    # instancio la clase Encaython y le paso como parametro la ventana(ventana)
    app = Encaython(ventana)
    ventana.mainloop()

