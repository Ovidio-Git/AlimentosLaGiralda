from flask import Flask, render_template, url_for,redirect,request
from markupsafe import escape
#para mejorar login
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, flash
# Formularios
from forms import Search, LogIn,Form
# Base de datos
from bdatos import ejecutar_sel, ejecutar_acc, ejecutar_sel_filter,ejecucucion_directa
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
    res2 = ejecutar_acc(sql2, (res, form["documento"], generate_password_hash(form["documento"]), 3))
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

# Ruta para realiza el login 
@app.route("/login/", methods=["GET","POST"])
def login():
    frm = LogIn()
    global sesion_iniciada      
                                
    if request.method == "GET":
        
        return render_template("login.html",form=frm, titulo='Login::Alimentos la Giralda')
    else:
        sesion_iniciada = True
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
            if check_password_hash(cbd,cla): 
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

# Ruta de empleados para mostrar los datos dela persona que realizado el login
@app.route('/empleado/<int:empleado>', methods=["GET"])
def Empleado(empleado):
    sql = 'SELECT * FROM empleados where idusuario = %s'% (empleado)
    res = ejecutar_sel(sql)
    if len(res)>0:
        return render_template('InfoUser.html', info = res[0])

# Ruta de administradores que lleva al formulario para crear nuevos empleados
@app.route('/crear', methods=["GET"])
def crear():
    form = Form()
    return render_template('crearusuario.html', form = form)

# Ruta de administradores para crear nuevos empleados
@app.route('/crear', methods=["POST"])
def accionCrear():
    if (crearEmpleado(request.form)):
        return redirect("/dashboard")
    return render_template('crearusuario.html', form = request.form)

# Ruta de administradores al tablero que muesta el conglomerado de empleados
@app.route('/dashboard', methods=["GET"])
def dashboard():
    sql = "SELECT * FROM empleados"
    res = ejecutar_sel(sql)
    empleados = obtenerTablaEmpleados(res)
    form = Search()
    return render_template('dashboard.html', data = {"empleados": empleados}, form = form)

# Ruta de administradores que realiza el filtrado de los datos de la tabla conglomerado de empleados
@app.route('/dashboard', methods=["POST"])
def search(): 
    form = Search()
    busqueda = searchEmpleado(request.form["name"])
    return render_template('dashboard.html', data = {"empleados": busqueda}, form = form)

# Ruta de administradores para editar los datos que se muestran en la tabla de conglomerado de empleados
@app.route('/editar', methods=('POST',))
def editar():
    nombre          = request.form.get('Nombre')
    Documento       = request.form.get('Documento')
    Apellido        = request.form.get('Apellido')
    Cargo           = request.form.get('Cargo')
    Area            = request.form.get('Area')
    Salario         = request.form.get('Salario')
    TipodeContrato  = request.form.get('TipodeContrato')
    FechaIngreso    = request.form.get('FechaIngreso')
    FechaTerminaciondecontrato  = request.form.get('FechaTerminaciondecontrato')
    Puntaje                     = request.form.get('Puntaje')
    Retroalimentacion           = request.form.get('Retroalimentacion')
    sql="""UPDATE empleados 
        SET nombre='%s',
            apellido='%s',
            cargo='%s',
            area='%s',
            puntaje=%s,
            retroalimentacion='%s',
            salario=%s,
            fecingreso='%s',
            fecterminacion='%s',
            tipocontrato='%s'  
        WHERE documento = %s"""% (nombre,Apellido,Cargo,Area,Puntaje,Retroalimentacion,Salario,FechaIngreso,FechaTerminaciondecontrato,TipodeContrato,Documento)
    ejecucucion_directa(sql)
    return redirect(url_for('dashboard'))

# Ruta de administradores que lleva al formulario para editar los datos de los empleados
@app.route('/editar/<int:documento_empleado>', methods=["GET"])
def paginaEditar(documento_empleado):
    sql = 'SELECT * FROM empleados WHERE documento = %s'% (documento_empleado)
    empleado = ejecutar_sel(sql)
    return render_template('editarusuario.html', empleados = empleado)

# Ruta de administradores para eliminar empleados de la tabla de conglomerado de empleados
@app.route('/delete/<int:documento_empleado>', methods=('POST',))
def delete(documento_empleado):
    sql='DELETE FROM empleados WHERE documento = %s'% (documento_empleado)
    ejecutar_sel(sql)
    return redirect(url_for('dashboard'))


if __name__=='__main__':
    app.run(debug=True)
