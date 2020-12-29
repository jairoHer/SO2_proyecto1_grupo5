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
import time

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
ruta = None
#clienteMongo= None
#104.197.235.139
clienteMongo = MongoClient('mongodb://104.197.235.139',port=27017)
#clienteMongo = MongoClient('mongoso2',port=27017)
#db = None
db = clienteMongo['proyecto1']
#coleccion = None
coleccion = db['videojuegos']
#usuarios = None
usuarios = db['usuarios']
usuario = ""

def crearConexion(direccion):
    try: 
        global clienteMongo
        clienteMongo = MongoClient('mongodb://'+direccion,port=27017)
        #clienteMongo = MongoClient('mongoso2',port=27017)
        global db
        db = clienteMongo['proyecto1']
        global coleccion
        coleccion = db['videojuegos']
        global usuarios
        usuarios = db['usuarios']
    except:
        print("fallo en conexion")

#esto ira al backend en forma de api despues


def ingresarUsuario(nombre,password):
    json_usuario = {
            "nombre" : nombre,
            "password" : password, 
        }
    response = ''
    while response == '':
        try:
            ip_address = request.host.split(':')[0]
            response = requests.post("http://"+str(ip_address)+":5001/registro", json=json_usuario)
            #response = requests.post("http://backend:5001/registro", json=json_usuario)
            solicitud = response.json()
            break
        except:
            time.sleep(1)
            continue
    
    #usuarios.insert_one({
    #    'nombre': nombre,
    #    'password': password,
    #    'juegos':[],
    #})

def verficarExistencia(nombre,password):
    dato = None
    valido = False
    while valido == False:
        try:
            dato=usuarios.find_one(
                {"nombre":nombre,"password":password},
                {"_id" : 0}
            )
            valido = True
            break
        except:
            time.sleep(1)
            ip_address = request.host.split(':')[0]
            ip_address = '104.197.235.139'
            crearConexion(str(ip_address))
            dato = None
            continue
    return dato
#--------

def obtenerDatos():
    #cursor = coleccion.find({})
    #videojuegos = []
    datos = []
    solicitud = ''
    while solicitud == '':
        try:
            ip_address = request.host.split(':')[0]
            solicitud = requests.get('http://'+str(ip_address)+':5001/disponibles', verify=False)
            #solicitud = requests.get('http://backend:5001/disponibles', verify=False)
            datos = solicitud.json()
            break
        except:
            time.sleep(1)
            continue
    #for documento in cursor:
    #    videojuegos.append({'author':documento['author'],'title':documento['title'],'content':documento['content'],'descargas':documento['descargas']})
        #print(documento['title'])
    #print(datos)
    #print("-----------------")
    #print(videojuegos)
    return datos
    #return videojuegos

def descarga(nombre):
    valido = False
    while valido == False:
        try:           
            coleccion.update(
                {'title':nombre},
                {'$inc':{'descargas':1}}
            )
            valido = True
            break
        except:
            time.sleep(1)
            ip_address = request.host.split(':')[0]
            ip_address = '104.197.235.139'
            crearConexion(str(ip_address))
            continue

def agregarJuego(usuario,nombre):
    print(usuario,nombre)
    json_usuario = {
            "nombre" : usuario,
            "juego" : nombre, 
        }
    response=''
    while response=='':
        try:
            ip_address = request.host.split(':')[0]
            response = requests.post("http://"+str(ip_address)+":5001/agregarJuego", json=json_usuario)
            #response = requests.post("http://backend:5001/agregarJuego", json=json_usuario)
            solicitud = response.json()
            break
        except:
            time.sleep(1)
            continue

    #usuarios.update(
    #    {'nombre':usuario},
    #    {'$push':{'juegos':{
    #                    'title': nombre,
    #                }    
    #            }
    #    }
    #)

def obtenerJuegosUsuario(usuario):
    valido = False
    while valido == False:
        try:
            dato=usuarios.find_one(
                {"nombre":usuario},
                {"_id" : 0,"password":0,"nombre":0}
            )
            valido=True
            break
        except:
            time.sleep(1)
            ip_address = request.host.split(':')[0]
            ip_address = '104.197.235.139'
            crearConexion(str(ip_address))
            continue
    #for juego in dato['juegos']:
    #    print(juego)
    #print(dato)
    return dato['juegos']

@app.route('/',methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    #return "<h1>Aqui estara los juegos</h1>"
    global ruta
    ip_address = request.host.split(':')[0]
    ruta = str(ip_address)
    if clienteMongo ==None:
        ip_address = '104.197.235.139'   
        crearConexion(str(ip_address))
        return '<h1>Preparando conexion mongo...</h1>'
    
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
    global ruta
    ip_address = request.host.split(':')[0]
    ip_address = '104.197.235.139'
    ruta = str(ip_address)
    if clienteMongo ==None:   
        crearConexion(str(ip_address))
    print("mi usuario es: "+usuario)
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
    global ruta
    ip_address = request.host.split(':')[0]
    ip_address = '104.197.235.139'
    ruta = str(ip_address)
    if clienteMongo ==None:   
        crearConexion(str(ip_address))
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
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=5000,debug=True)
