from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def saludar():
    return '<h1 style="text-aling:center;">Que hay de nuevo viejo?</h1>'

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__=='__main__':
    app.run(debug=True)
