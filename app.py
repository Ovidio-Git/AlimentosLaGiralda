from flask import Flask, render_template
from flask import request
from utils.jsonUtils import loadStartData
from forms import Search

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def searchEmpleado(text, empleados):
    resultado = []

    if (text == ''):
        return empleados

    for empleado in empleados:
        if (empleado['nombre'] == text):
            resultado.append(empleado)

    return resultado

@app.route('/')
def saludar():
    return '<h1 style="text-aling:center;">Alimentos La Giralda</h1>'

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
