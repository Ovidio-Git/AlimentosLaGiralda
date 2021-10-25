from flask import Flask, render_template
from flask import request
from utils.jsonUtils import loadStartData
from markupsafe import escape

# Formularios
from forms import Search
from forms import LogIn
from forms import Form

from flask import redirect


import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ----------------variables globales
sesion_iniciada = False   #Creamos esta variable con su valor inicial para validar


# ---------------- Funciones
def searchEmpleado(text, empleados):
    resultado = []

    if (text == ''):
        return empleados

    for empleado in empleados:
        if (empleado['documento'] == text):
            resultado.append(empleado)

    return resultado

def crearEmpleado(form, empleados):
    nuevoEmpleado = {
        'nombre': form["nombre"],
        "apellido": form["apellido"],
        "documento": form["documento"],
        "cargo":form["cargo"],
        "fecIngreso": form["fecIngreso"],
        "tipContrato": form["tipoContrato"],
        "terminacion": form["terminacion"],
        "area": form["area"],
        "salario": form["salario"],
        "retro": form["retro"],
        "puntaje": form["puntaje"],
        "tipoUsuario": "Empleado"
    }

    empleados.append(nuevoEmpleado)
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

@app.route('/empleado/', methods=["GET","POST"]) # agrego la ruta de empleado
def Empleado():
    data = loadStartData.data
    form = Search()
    if request.method == "GET":
        return render_template('InfoUser.html', form = form, data = data)
    elif request.method == "POST":
        return render_template('InfoUser.html', form = form, data = data)

@app.route('/dashboard')
def dashboard():
    global data
    data = loadStartData.data
    form = Search()
    return render_template('dashboard.html', data = data, form = form)

@app.route('/buscar', methods=["POST"])
def search():
    form = Search()
    busqueda = searchEmpleado(request.form["name"], data['empleados'])
    return render_template('dashboard.html', data = {"empleados": busqueda}, form = form)

@app.route('/crear', methods=["GET"])
def crear():
    form = Form()
    return render_template('layout.html', form = form)

@app.route('/crear', methods=["POST"])
def accionCrear():
    if (crearEmpleado(request.form, data['empleados'])):
        return redirect("/dashboard")

    return render_template('layout.html', form = request.form)

if __name__=='__main__':
    app.run(debug=True)
