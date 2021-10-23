"""
Trabajar con la base de datos real.

   Consultas de acción ::   Modifican la base de datos y reportan la 
                            cantidad de filas que fueron afectadas (int)

   Consultas de selección   Recuperan información de la base de datos 
                            y retornan los registros  (list - RecordSet, ResultSet)
"""
import sqlite3

NOM_BD = 'bdc0332.db'

def ejecutar_acc(sql) -> int:
    """ Ejecuta consultas de accion : INSERT, DELETE, UPDATE """
    try:
        with sqlite3.connect(NOM_BD) as con:  # Conectarse a la base de datos
            cur = con.cursor()                # Crea un área intermedia para gestión de los contenidos
            res = cur.execute(sql).rowcount   # Ejecutar la consulta
            if res!=0:                        # Verificar si se realizó algún cambio
                con.commit()                  # Volver permanente el cambio
    except:
        res = 0
    return res

def ejecutar_sel(sql) -> list:
    """ Ejecuta consultas de seleccion : SELECT """
    try:
        with sqlite3.connect(NOM_BD) as con:  # Conectarse a la base de datos
            cur = con.cursor()                # Crea un área intermedia para gestión de los contenidos
            res = cur.execute(sql).fetchall() # Se obtienen los registros devueltos
    except:
        res = None
    return res
