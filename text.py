from sqlite3.dbapi2 import Error
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter.messagebox import *

class Encaython:
    # db_name='database.db'
    db_name='database'

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
        self.crea_tabla()
        self.menu() #llamo los botones de menu

    def menu(self):
        
        menu=Frame(self.root)
        menu.grid(row=0, column=0,sticky=W)
        agrega=Button(menu,text='Agregar Contenido',command=self.menu_agrega_contenido)
        agrega.grid(row=1,column=0,pady=5,sticky=W)
        conten=Button(menu,text='Ver Contenido',command=self.menu_contenido)
        conten.grid(row=1, column=1,pady=5,sticky=W)
        
    def menu_contenido(self):
        try:
            agrega.destroy()
        except:
            pass
        global contenido
        contenido=Frame(self.root)
        contenido.grid(row=1, column=0,columnspan=3,pady=20,padx=20)
        self.frame=LabelFrame(contenido, text='Ver contenido')
        self.frame.grid(row=1, column=0,columnspan=3,pady=20,padx=20)
        # input titulo
        Label(self.frame,text='Titulo:').grid(row=0, column=0)
        self.e_titulo=Entry(self.frame,state='disabled',disabledbackground='gray')
        self.e_titulo.grid(row=0,column=1,sticky=W+E)
        
        # input codigo
        Label(self.frame,text='Codigo:').grid(row=1, column=0)
        self.e_codigo=Text(self.frame,state='disabled',bg='gray')
        self.e_codigo.grid(row=1, column=1)

                # input codigo
        Label(self.frame,text='Resultado:').grid(row=2, column=0)
        self.e_resultado=Text(self.frame,state='disabled',bg='gray')
        self.e_resultado.grid(row=2, column=1)
        #    ventana ver contenido
        self.listbox = Listbox(self.frame)
        self.listbox.grid(row=1,column=3,rowspan=2,sticky=W+E+N+S,padx=20)
        lb_b_e=Frame(self.frame)
        lb_b_e.grid(row=0,column=3, columnspan=2,pady=5,padx=10,sticky=W+E+N+S)
        btn_borrar=Button(lb_b_e,text='Borrar',command=self.borrar)
        btn_borrar.grid(row=0,column=0,pady=5,padx=10,sticky=W+E+N+S)
        btn_editar=Button(lb_b_e,text='Editar',command=self.menu_editar)
        btn_editar.grid(row=0,column=1,pady=5,padx=10,sticky=W+E+N+S)


        self.obtener_titulos()
    
    def menu_editar(self):
        self.editar()
        global contenedor2
        contenedor2=Toplevel()
        contenedor2.title='Editar contenido'

        contenedor2.grid()

        #------- creamos canvas -------
        mi_canvas = Canvas(contenedor2)
        mi_canvas.pack(side=LEFT,fill=BOTH,expand=1)


        # ------- agregamos Scrollbar  a canvas 

        mi_scrollbar = ttk.Scrollbar(contenedor2, orient=VERTICAL,command=mi_canvas.yview)
        mi_scrollbar.pack(side=RIGHT, fill=Y)


        #--------- configuro canvas ----
        mi_canvas.configure(yscrollcommand=mi_scrollbar.set)
        mi_canvas.bind('<Configure>', lambda e: mi_canvas.configure(scrollregion= mi_canvas.bbox('all')))

        # ---------- creamos otro frame dentro de canvas
        root= Frame(mi_canvas)

        # ---------- agregamos este ultimo frame al canvas
        mi_canvas.create_window((0,0), window=root,anchor='nw')


        #----------------aqui va el codigo (ejemplo de prueba)

        self.frame2=LabelFrame(root, text='Editar contenido')
        self.frame2.grid(row=1, column=0,columnspan=3,pady=20,padx=20)
        # input titulo
        Label(self.frame2,text='Titulo:').grid(row=0, column=0)
        self.e_titulo2=Entry(self.frame2)
        self.e_titulo2.insert(0,self.edit_tit)
        self.e_titulo2.grid(row=0,column=1,sticky=W+E)
        
        # input codigo
        Label(self.frame2,text='Codigo:').grid(row=1, column=0)
        self.e_codigo2=Text(self.frame2)
        self.e_codigo2.insert(INSERT,self.edit_codigo)
        self.e_codigo2.grid(row=1, column=1)

                # input codigo
        Label(self.frame2,text='Resultado:').grid(row=2, column=0)
        self.e_resultado2=Text(self.frame2)
        self.e_resultado2.insert(INSERT,self.edit_resul)
        self.e_resultado2.grid(row=2, column=1)
        #    ventana ver contenido
        lb_b_e2=Frame(self.frame2)
        lb_b_e2.grid(row=0,column=3, columnspan=2,pady=5,padx=10,sticky=W+E+N+S)
        btn_editar2=Button(lb_b_e2,text='Aceptar',command=self.guarda_edicion)
        btn_editar2.grid(row=0,column=1,pady=5,padx=10,sticky=W+E+N+S)

    def menu_agrega_contenido(self):
        try:
            contenido.destroy()
        except:
            pass
        global agrega
        agrega=Frame(self.root)
        agrega.grid(row=1, column=0,columnspan=3,pady=20,padx=20)
        self.frame=LabelFrame(agrega, text='Cargar contenido')
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

        Button(self.frame,text='Agregar',command=self.agregar_contenido).grid(row=0,column=3, columnspan=2,pady=5,padx=10,sticky=W+E)

        #    ventana ver contenido
        self.listbox = Listbox(self.frame)
        self.listbox.grid(row=1,column=3,rowspan=3,sticky=W+E+N+S,padx=20)


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
            "titulo"	TEXT NOT NULL,
            "codigo"	TEXT NOT NULL,
            "resultado"    TEXT,
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

    def validacion(self):
        return ((len(self.e_titulo.get())) !=0 and (len(self.e_codigo.get(1.0,END)) !=1) )
    
    def agregar_contenido(self):
        # valido los campos
        if self.validacion():
            #genero la query
            query= 'INSERT INTO sql VALUES(NULL,?,?,?)'
            parametros=(self.e_titulo.get(),self.e_codigo.get(1.0,END),self.e_resultado.get(1.0,END))
            self.hacer_consluta(query,parametros)
            self.obtener_titulos()
            showinfo(title='Agregar', message=f'{self.e_titulo.get()} agregado correctamente')
            #borramos contenido de los entrys
            self.e_titulo.delete(0,END)
            #TODO borrar el contenido del text
            self.e_codigo.delete(1.0,END) 
            self.e_resultado.delete(1.0,END)
        else:
            showerror(title='Error en formulario',message='Los campos título y código son requeridos, verifique los datos e inténtelo nuevamente')

    def listar_tablas(self):
        query=f'''SELECT * FROM sqlite_master WHERE type = "table"'''
        lista_tablas=self.hacer_consluta(query)
        for lista in lista_tablas:
            print(lista)

    def borrar(self):
        try:
            parametros= self.listbox.get(self.listbox.curselection())
            query= "DELETE FROM sql WHERE titulo = ?"
            self.hacer_consluta(query,(parametros,))
            print(type(str(parametros,)))
            showinfo(title='Borrar',message=f'{parametros} borrado correctamente')
            self.obtener_titulos()

        except TclError:
            showerror(title='ERROR',message='No seleccionaste elemento de la lista')
        
    def editar(self):
        try:
            self.edit_tit=''
            self.edit_codigo=''
            self.edit_resul=''
            parametros= self.listbox.get(self.listbox.curselection())
            query= "SELECT * FROM sql WHERE titulo = ?"
            self.fila_db=self.hacer_consluta(query,(parametros,))
            for fila in self.fila_db:
                self.edit_tit=fila[1]
                self.edit_codigo=fila[2]
                self.edit_resul=fila[3]
            # showinfo(title='Borrar',message=f'{parametros} borrado correctamente')
            self.obtener_titulos()

        except TclError:
            showerror(title='ERROR',message='No seleccionaste elemento de la lista')

    def guarda_edicion(self):
        try:
            viejo_titulo=self.edit_tit
            nuevo_titulo=self.e_titulo2.get()
            nuevo_codigo=self.e_codigo2.get(1.0,END)
            nuevo_resultado=self.e_resultado2.get(0.0,END)
            print(nuevo_resultado)
            parametros =(nuevo_titulo,nuevo_codigo,nuevo_resultado,viejo_titulo)
            query="UPDATE sql SET titulo= ?, codigo= ?, resultado= ? WHERE titulo= ?"
            self.hacer_consluta(query,parametros)
            self.obtener_titulos()
        except Error as e:
            print(e)
        contenedor2.destroy()
        # TODO me quede en la consulta de actualizacion

if __name__ == '__main__':
    ventana = Tk()
    # instancio la clase Encaython y le paso como parametro la ventana(ventana)
    app = Encaython(ventana)
    ventana.mainloop()

