from datetime import datetime
from flask import Flask,request,jsonify, render_template, url_for, flash, redirect
from flask_cors import CORS
from pymongo import MongoClient
import pymongo
import requests
import json
import socket
import time

app = Flask(__name__)
CORS(app)
#urlmongo = request.host.split(':')[0]
#clienteMongo= None
ruta = None
#clienteMongo = MongoClient('mongodb://'+str(socket.getfqdn()),port=27017)
#clienteMongo = MongoClient(str(socket.getfqdn()),port=27017)
#clienteMongo = MongoClient('mongoso2',port=27017)
#clienteMongo = MongoClient('localhost',port=27017)
clienteMongo = MongoClient('mongodb://104.197.235.139',port=27017)
#db = None
db = clienteMongo['proyecto1']
#coleccion = None
coleccion = db['videojuegos']
#usuarios = None
usuarios = db['usuarios']

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

def ingresarUsuario(nombre,password):
    valido = False
    while valido == False:
        try:
            usuarios.insert_one({
                'nombre': nombre,
                'password': password,
                'juegos':[],
            })
            valido = True
            break
        except:
            time.sleep(1)
            ip_address = request.host.split(':')[0]
            ip_address ='104.197.235.139'
            crearConexion(str(ip_address))
            continue
            #print('no se pudo ingresar el usuario')

def agregarGame(usuario,nombre):
    print(usuario,nombre)
    valido = False
    while valido == False:
        try:
            usuarios.update(
                {'nombre':usuario},
                {'$push':{'juegos':{
                                'title': nombre,
                            }    
                        }
                }
            )
            valido = True
            break
        except:
            time.sleep(1)
            ip_address = request.host.split(':')[0]
            ip_address ='104.197.235.139'
            crearConexion(str(ip_address))
            continue
        #print('no se pudo agregar juego a lista de usuario')

def darJuegosDisponibles():
    valido = False
    datos = []
    while valido == False:
        try:
            cursor = coleccion.find({})
            #datos = []
            for documento in cursor:
                datos.append({'author':documento['author'],'title':documento['title'],'content':documento['content'],'descargas':documento['descargas']})
            valido = True
            break
        except:
            time.sleep(1)
            ip_address = request.host.split(':')[0]
            ip_address ='104.197.235.139'
            crearConexion(str(ip_address))
            continue
    return datos

@app.route('/disponibles',methods=['GET'])
def disponibles():
    global ruta
    ip_address = request.host.split(':')[0]
    ip_address ='104.197.235.139'
    ruta = str(ip_address)
    if clienteMongo ==None:   
        crearConexion(str(ruta))
    if clienteMongo !=None:
        #cursor = coleccion.find({})
        datos = darJuegosDisponibles()
        #for documento in cursor:
        #    datos.append({'author':documento['author'],'title':documento['title'],'content':documento['content'],'descargas':documento['descargas']})

        return jsonify(datos)
    else:
        return jsonify(
            estado='Error de conexion con mongo'
        )

@app.route('/agregarJuego',methods=['POST'])
def agregarJuego():
    global ruta
    ip_address = request.host.split(':')[0]
    ip_address ='104.197.235.139'
    ruta = str(ip_address)
    if clienteMongo ==None:   
        crearConexion(str(ruta))
    solicitud = request.get_json(force=True, silent = True)
    if solicitud == None:
        return jsonify(
                    estado='500',
                    mensaje='Existe un error en la estructura del JSON con el que se hace la solicitud ',
                   )
    usuario = solicitud.get('nombre')
    nombre = solicitud.get('juego')
    #insercion(autor,nota)
    agregarGame(usuario,nombre)
    print("se recibio en el request a: "+usuario)
    return jsonify(
        estado='Mensaje recibido'
    )

@app.route('/registro',methods=['POST'])
def registro():
    global ruta
    ip_address = request.host.split(':')[0]
    ip_address ='104.197.235.139'
    ruta = str(ip_address)
    if clienteMongo ==None:   
        crearConexion(str(ruta))
    solicitud = request.get_json(force=True, silent = True)
    if solicitud == None:
        return jsonify(
                    estado='500',
                    mensaje='Existe un error en la estructura del JSON con el que se hace la solicitud ',
                   )
    usuario = solicitud.get('nombre')
    passw = solicitud.get('password')
    #insercion(autor,nota)
    ingresarUsuario(usuario,passw)
    print("se recibio en el request a: "+usuario)
    return jsonify(
        estado='Mensaje recibido'
    )

@app.route('/')
def hello():
    global ruta
    ip_address = request.host.split(':')[0]
    ip_address ='104.197.235.139'
    ruta = str(ip_address)
    if clienteMongo ==None:   
        crearConexion(str(ip_address))
        return '<h1>Este es el servidor backend</h1>'
    else:
        return '<h1>Este es el backend</h1>'
    #return '<h1>Api back '+str(ip_address)+'</h1>'

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0',port=5001)
