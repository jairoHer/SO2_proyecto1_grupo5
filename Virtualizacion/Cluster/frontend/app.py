from datetime import datetime
from flask import Flask,request, render_template, url_for, flash, redirect
from flask_cors import CORS
from pymongo import MongoClient
from forms import Registro, Login
import pymongo
import requests
import json
import os
import socket

juegos=[
    {
        'author':'Jairo Hernandez',
        'title': 'GTA V',
        'content':'Juego de hacer cosas malas, pero divertido',
        'descargas':'22',

    },
    {
        'author':'Pablo Hernandez',
        'title': 'Dark Souls',
        'content':'Juego donde a ley te vas a morir',
        'descargas':'10',
    }
]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e9d830bde37db8ca424cb0b55af9dac2'
CORS(app)

clienteMongo = MongoClient('mongoso2',port=27017)
db = clienteMongo['proyecto1']
coleccion = db['videojuegos']

usuarios = db['usuarios']
usuario = ""

#esto ira al backend en forma de api despues


def ingresarUsuario(nombre,password):
    json_usuario = {
            "nombre" : nombre,
            "password" : password, 
        }
    response = requests.post("http://backend:5001/registro", json=json_usuario)
    solicitud = response.json()
    
    #usuarios.insert_one({
    #    'nombre': nombre,
    #    'password': password,
    #    'juegos':[],
    #})

def verficarExistencia(nombre,password):
    dato=usuarios.find_one(
        {"nombre":nombre,"password":password},
        {"_id" : 0}
    )
    return dato
#--------

def obtenerDatos():
    #cursor = coleccion.find({})
    #videojuegos = []

    solicitud = requests.get('http://backend:5001/disponibles', verify=False)
    datos = solicitud.json()

    #for documento in cursor:
    #    videojuegos.append({'author':documento['author'],'title':documento['title'],'content':documento['content'],'descargas':documento['descargas']})
        #print(documento['title'])
    #print(datos)
    #print("-----------------")
    #print(videojuegos)
    return datos
    #return videojuegos

def descarga(nombre):
    coleccion.update(
        {'title':nombre},
        {'$inc':{'descargas':1}}
    )

def agregarJuego(usuario,nombre):
    print(usuario,nombre)
    json_usuario = {
            "nombre" : usuario,
            "juego" : nombre, 
        }
    response = requests.post("http://backend:5001/agregarJuego", json=json_usuario)
    solicitud = response.json()

    #usuarios.update(
    #    {'nombre':usuario},
    #    {'$push':{'juegos':{
    #                    'title': nombre,
    #                }    
    #            }
    #    }
    #)

def obtenerJuegosUsuario(usuario):
    dato=usuarios.find_one(
        {"nombre":usuario},
        {"_id" : 0,"password":0,"nombre":0}
    )
    for juego in dato['juegos']:
        print(juego)
    print(dato)
    return dato['juegos']

@app.route('/',methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    #return "<h1>Aqui estara los juegos</h1>"
    global usuario
    print(juegos)
    videojuegos = obtenerDatos()
    if request.method=="POST":
        if usuario == "":
            flash(f'Debes estar logeado para descargar', 'danger')
            return redirect(url_for('home'))
        print('se detecto data '+ request.form['juego'])
        jueguito =str(request.form['juego'])
        flash(f'Se ha descargado {jueguito} exitosamente', 'success')
        descarga(request.form['juego'])
        agregarJuego(usuario,request.form['juego'])
    return render_template('home.html', juegos=videojuegos)

@app.route('/juegos',methods=['GET','POST'])
def juegos():
    print("mi usuario es: "+usuario)
    videojuegos = obtenerDatos()
    if usuario=="":
        flash(f'Debe estar logeado para ver sus juegos', 'danger')
        return redirect(url_for('home'))
    juegs = obtenerJuegosUsuario(usuario)
    return render_template('juegos.html', juegos=juegs,usuario=usuario)

@app.route("/register", methods=['GET','POST'])
def register():
    form = Registro()
    if form.validate_on_submit():
        ingresarUsuario(form.usuario.data,form.password.data)
        flash(f'Cuenta creada para {form.usuario.data}', 'success')

        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = Login()
    global usuario
    if form.validate_on_submit():
        if form.usuario.data != '' and form.password.data != '':
            usuario_l = verficarExistencia(form.usuario.data,form.password.data)
            if usuario_l == None:
                flash(f'Usuario o contraseña incorrectas {form.usuario.data}', 'danger')
            else:
                flash('Estas logueado!', 'success')
                usuario = form.usuario.data
                print("usuario logueado: "+usuario)
                return redirect(url_for('home'))
            #print(usuario_l)
            #print('logueado '+form.usuario.data)
    return render_template('login.html', title='Login', form=form)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
