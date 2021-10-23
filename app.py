from flask import Flask, render_template
from flask import request
from utils.jsonUtils import loadStartData
from markupsafe import escape

# Formularios
from forms import Search
from forms import LogIn
from forms import Form

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
            "documento":    row[1],
            'nombre':       row[2],
            "apellido":     row[3],
            "cargo":        row[10],
            "fecIngreso":   row[6],
            "tipContrato":  row[8],
            "terminacion":  row[7],
            "area":         "",
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
    else:
        return True


# ----------------A partir de aqui las rutas -------------------
@app.route('/')
@app.route('/home/')
@app.route('/index/')
def main():
    return render_template('home.html', titulo='Home::Alimentos la Giralda')


@app.route("/login/", methods=["GET","POST"])
def login():
    frm = LogIn()
    global sesion_iniciada      
                                
    if request.method == "GET":
        
        return render_template("login.html",form=frm, titulo='Login::Alimentos la Giralda')
      
    else:
        sesion_iniciada = True
        #recuperar los datos del formulario
        
        log = escape(request.form['usr']) 
        cla = escape(request.form['pwd'])
        #validar los datos
        if len(log.strip())==0:
            pass#flash('Por favor diligencie el usuario')
        if len(cla.strip())==0:
            pass#flash('Por favor diligencie la clave')
            
        if log=='administradorAG' and cla=='123456789':
            #flash('Acceso concedido')
            return redirect("/dashboard") # redirecciona a /dashboard
            #return "<h1>Entro Administrador</h1>" #para probar logica de forma individual
            
        if log== 'empleadoAG' and cla=='123456789':
            #flash('Acceso concedido') 
            #return redirect("/empleado") # redirecciona a /Empleado
            return "<h1>Entro Empleado</h1>"
        else:
            #flash('Usuario o clave invalidos')
            return "<h1>Parece que Tienes un Usuario o contraseña equivocados</h1>"
        
        #frm=LogIn() #creo un objeto para el formulario

        #return redirect("/donde_sea") # redirecciona a /donde_sea

#@app.route('/empleado')
    

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

@app.route('/crear', methods=["GET"])
def crear():
    form = Form()
    return render_template('crearusuario.html', form = form)

@app.route('/crear', methods=["POST"])
def accionCrear():
    if (crearEmpleado(request.form)):
        return redirect("/dashboard")

    return render_template('crearusuario.html', form = request.form)

if __name__=='__main__':
    app.run(debug=True, port=80)
