from datetime import datetime
from flask import Flask,request,jsonify, render_template, url_for, flash, redirect
from flask_cors import CORS
from pymongo import MongoClient
import pymongo
import requests
import json
import socket

app = Flask(__name__)
CORS(app)

clienteMongo = MongoClient('mongodb://'+str(socket.getfqdn()),port=27017)
#clienteMongo = MongoClient(str(socket.getfqdn()),port=27017)
#clienteMongo = MongoClient('mongoso2',port=27017)
#clienteMongo = MongoClient('localhost',port=27017)
db = clienteMongo['proyecto1']
coleccion = db['videojuegos']

usuarios = db['usuarios']

def ingresarUsuario(nombre,password):
    usuarios.insert_one({
        'nombre': nombre,
        'password': password,
        'juegos':[],
    })

def agregarGame(usuario,nombre):
    print(usuario,nombre)
    usuarios.update(
        {'nombre':usuario},
        {'$push':{'juegos':{
                        'title': nombre,
                    }    
                }
        }
    )

@app.route('/disponibles',methods=['GET'])
def disponibles():
    cursor = coleccion.find({})
    datos = []
    for documento in cursor:
        datos.append({'author':documento['author'],'title':documento['title'],'content':documento['content'],'descargas':documento['descargas']})

    return jsonify(datos)

@app.route('/agregarJuego',methods=['POST'])
def agregarJuego():
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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    myip = s.getsockname()[0]
    s.close()
    ip_address = request.remote_addr
    cosa = str(socket.getfqdn())
    return '<h1>Api back '+str(ip_address)+'</h1>'

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0',port=5001)
