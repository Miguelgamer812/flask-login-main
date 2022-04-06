from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
conexion = MySQL(app) #Conexión a base de datos tras importar el módulo
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(conexion, id)


@app.route('/') # Indicamos la ruta inicial
def index():#Indicamos el nombre de una vista
    return redirect(url_for('login')) #Nos retorna una plantilla o template

@app.route('/login', methods=['GET', 'POST']) #Esta ruta permite hacer uso de ambos métodos
def login():
    if request.method == 'POST': #Si lo requerimos por medio de POST si lo enviamos
         #print(request.form['user'])
         #print(request.form['password'])
        """cursor=conexion.connection.cursor()
        sql="SELECT usuario, contraseña FROM user"
        cursor.execute(sql)
        datos=cursor.fetchall()
        print(datos)"""
        usuarios = User(0, request.form['usuario'], request.form['contraseña'])#Obtenemos el name de los campos HTML
        logged_user = ModelUser.login(conexion, usuarios)
        if logged_user != None:
            if logged_user.contraseña != None:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta.")
                return render_template('auth/login.html') #Acciones por GET
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/listar') #preestablecemos la ruta raiz y el método
def listar(): # Creamos la funcion listar
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT id, usuario, contraseña, fullname FROM user"
        cursor.execute(sql)
        datos=cursor.fetchall()
        listar=[]
        for fila in datos:
            lista = {'id':fila[0], 'usuario':fila[1], 'contraseña':fila[2], 'fullname':fila[3]}#Creamos diccionario para almacenar los datos en JSON
            listar.append(lista)
            
            
        return jsonify({'listar':listar,'mensaje':"Usuarios listados."})#Retornamos el Json con la consulta

    except Exception as e:
        return jsonify({'mensaje':"Error"})


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])#Organizamos las configuraciones para desarrollar
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()# Enciende la app


