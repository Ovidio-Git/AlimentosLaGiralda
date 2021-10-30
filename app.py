from flask import Flask, render_template, url_for
from flask import request
from markupsafe import escape

#para mejorar login
from werkzeug.security import check_password_hash
from flask import session, flash

# Formularios
from forms import Search
from forms import LogIn
from forms import Form,Form2

# Base de datos
from bdatos import ejecutar_sel, ejecutar_acc, ejecutar_sel_filter

from flask import redirect


import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ----------------variables globales
sesion_iniciada = False   #Creamos esta variable con su valor inicial para validar


# ---------------- Funciones
def searchEmpleado(text):

    nombre = "%" + text + "%"
    sql = "SELECT * FROM empleados WHERE documento = ? or nombre like ? or apellido like ?"
    res = ejecutar_sel_filter(sql, (text, nombre, nombre))

    empleados = obtenerTablaEmpleados(res)

    return empleados

def obtenerTablaEmpleados(datos):
    empleados = []

    for row in datos:
        empleado = {
            "id":           row[0],
            "documento":    row[1],
            'nombre':       row[2],
            "apellido":     row[3],
            "cargo":        row[10],
            "fecIngreso":   row[6],
            "tipContrato":  row[8],
            "terminacion":  row[7],
            "area":         row[13],
            "salario":      row[9],
            "retro":        row[11],
            "puntaje":      row[12]
        }
        empleados.append(empleado)
    return empleados

def crearEmpleado(form):

    sql = """INSERT INTO empleados (documento, nombre, apellido, edad, profesion, fecingreso, fecterminacion, tipocontrato, salario, cargo, retroalimentacion, puntaje)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"""

    
    nuevoEmpleado = (form["documento"], form["nombre"], form["apellido"], "20", "", form["fecIngreso"], form["terminacion"]
    , form["tipoContrato"], form["salario"], form["cargo"], form["retro"], form["puntaje"])

    res = ejecutar_acc(sql, nuevoEmpleado)

    if res == 0:
        return False

    sql2 = """INSERT INTO usuarios VALUES (?,?,?,?);"""
    res2 = ejecutar_acc(sql2, (res, form["documento"], form["documento"], 3))

    if res2 == 0:
        return False
    else:
        return True


# ----------------A partir de aqui las rutas -------------------
@app.route('/')
@app.route('/home/')
@app.route('/index/')
def main():
    return render_template('home.html', titulo='Home::Alimentos la Giralda')

# Ruta de Login
@app.route("/login/", methods=["GET","POST"])
def login():
    frm = LogIn()
    global sesion_iniciada      
                                
    if request.method == "GET":
        
        return render_template("login.html",form=frm, titulo='Login::Alimentos la Giralda')
      
    else:
        sesion_iniciada = True
        #recuperar los datos del formulario
        #log = escape(request.form['usr']) 
        #cla = escape(request.form['pwd'])

        # se incluyen secuencias de escape para mitigar el riesgo de inyeccion de codigo
        usu = escape(frm.usr.data.strip())
        cla = escape(frm.pwd.data.strip())

        #Preparo la consulta
        sql = f"SELECT Idusuario, contrasena, id_rol FROM Usuarios WHERE Usuario='{usu}'"
        #Ejecuto la consulta
        res = ejecutar_sel(sql)
        #valido el resultado
        if len(res)>0:
            #recupero la clave que viene de la base de datos
            cbd = res[0][1]
            #compruebo la clave --- debo importar ::  from werkzeug.security import check_password_hash
            #check_password_hash(cbd,cla):
            if cbd == cla: # Lo uso asi por que no tengo en este momento para crear las contrasenas con hash
                #Cargo los datos en una variable de sesion -- tengo que importarla con:: from flask import session
                # y queda la informacion disponible para compartirlas con otros modulos de la aplicacion
                session.clear()     #limpio la sesion
                session['id'] = res[0][0]
                session['usr'] = usu
                session['pwd'] = cla
                session['rol'] = res[0][2]

                if session['rol']==3:
                    return redirect('/empleado/%s'% session['id']) # redirecciona a /empleado
                
                elif session['rol']==2 or session['rol']==1:
                    return redirect("/dashboard") # redirecciona a /empleado
                
                else:
                    flash('ERROR:: Problemas con tu rol ...')
                    return render_template("login.html",form=frm, titulo='-Ingreso-::Alimentos la Giralda')
           
            else:
                flash('ERROR: clave invalida ...')
                return render_template("login.html",form=frm, titulo='Ingreso::Alimentos la Giralda')

        else:
            flash('Usuario o Clave no valida ...')
            return render_template("login.html",form=frm, titulo='Ingreso::Alimentos la Giralda')

@app.route('/empleado/<int:empleado>', methods=["GET"]) # agrego la ruta de empleado
def Empleado(empleado):
    sql = 'SELECT * FROM empleados where idusuario = %s'% (empleado)
    res = ejecutar_sel(sql)

    if len(res)>0:
        return render_template('InfoUser.html', info = res[0])

@app.route('/dashboard', methods=["GET"])
def dashboard():

    sql = "SELECT * FROM empleados"
    res = ejecutar_sel(sql)

    empleados = obtenerTablaEmpleados(res)

    form = Search()
    return render_template('dashboard.html', data = {"empleados": empleados}, form = form)

@app.route('/dashboard', methods=["POST"])
def search(): 
    form = Search()
    busqueda = searchEmpleado(request.form["name"])
    return render_template('dashboard.html', data = {"empleados": busqueda}, form = form)


@app.route('/editar', methods=('POST',))
def editar():
    # RECEIVE FORM DATA
    nombre  = request.form.get('Nombre')
    Documento  = request.form.get('Documento')
    print("documentales prro: ", Documento)
    print("nombre prro: ", nombre)
    Apellido  = request.form.get('Apellido')
    Cargo  = request.form.get('Cargo')
    Area  = request.form.get('Area')
    Salario  = request.form.get('Salario')
    TipodeContrato  = request.form.get('TipodeContrato')
    FechaIngreso  = request.form.get('FechaIngreso')
    FechaTerminaciondecontrato  = request.form.get('FechaTerminaciondecontrato')
    Puntaje  = request.form.get('Puntaje')
    Retroalimentacion  = request.form.get('Retroalimentacion')
    sql=f'UPDATE empleados SET nombre={nombre},apellido={Apellido},cargo={Cargo},Area={Area},puntaje={Puntaje},retroalimentación={Retroalimentacion},salario={Salario},fecingreso={FechaIngreso},fecterminacion={FechaTerminaciondecontrato},tipodeContrato={TipodeContrato}  WHERE documento = {Documento}'
    print("sql query", sql)
    ejecutar_sel(sql)
    return redirect(url_for('dashboard'))

@app.route('/editar/<int:documento_empleado>', methods=["GET"])
def paginaEditar(documento_empleado):
    sql = 'SELECT * FROM empleados WHERE documento = %s'% (documento_empleado)
    empleado = ejecutar_sel(sql)
    print("data", empleado[0][1])
    #empleados = obtenerTablaEmpleados(res)
    return render_template('editarusuario.html', empleados = empleado)

@app.route('/delete/<int:documento_empleado>', methods=('POST',))
def delete(documento_empleado):
    print("documento empleado", documento_empleado)
    sql='DELETE FROM empleados WHERE documento = %s'% (documento_empleado)
    ejecutar_sel(sql)
    return redirect(url_for('dashboard'))

@app.route('/crear', methods=["GET"])
def crear():
    form = Form()
    return render_template('crearusuario.html', form = form)

@app.route('/crear', methods=["POST"])
def accionCrear():
    if (crearEmpleado(request.form)):
        return redirect("/dashboard")

    return render_template('crearusuario.html', form = request.form)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
