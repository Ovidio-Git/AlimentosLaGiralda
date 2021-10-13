from flask import Flask, render_template
from flask import request
from utils.jsonUtils import loadStartData
from forms import Search
from forms import LogIn
from markupsafe import escape

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ----------------variables globales
sesion_iniciada = False   #Creamos esta variable con su valor inicial para validar

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
            flash('Por favor diligencie el usuario')
        if len(cla.strip())==0:
            flash('Por favor diligencie la clave')
        if log=='wilbhert' and cla=='123456789':
            flash('Acceso concedido')

            #return redirect("/usuario") # redirecciona a /usuario
            return "<h1>Entro Administrador</h1>"
        if log=='Adrian' and cla=='123456789':
            flash('Acceso concedido')

            #return redirect("/usuario") # redirecciona a /usuario
            return "<h1>Entro Empleado</h1>"
        else:
            flash('Usuario o clave invalidos')
            return "<h1>Parece que Tienes un Usuario o contraseña equivocados</h1>"
        
        #frm=LogIn() #creo un objeto para el formulario

        #return redirect("/donde_sea") # redirecciona a /donde_sea


def searchEmpleado(text, empleados):
    resultado = []

    if (text == ''):
        return empleados

    for empleado in empleados:
        if (empleado['nombre'] == text):
            resultado.append(empleado)

    return resultado

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

@app.route('/crear')
def crear():
    return render_template('layout.html')


if __name__=='__main__':
    app.run(debug=True)
