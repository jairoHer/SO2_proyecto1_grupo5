from pymongo import MongoClient
import pymongo
import requests
import json
import os

clienteMongo = MongoClient('localhost',port=27017)
db = clienteMongo['proyecto1']
coleccion = db['videojuegos']

def ingresarJuego(nombre, autor, contenido):
    coleccion.insert_one({
        'author': autor,
        'title': nombre,
        'content':contenido,
        'descargas':0,
    })

def verDatos():
    cursor = coleccion.find({})
    for documento in cursor:
        print(documento)

class ingreso():
    val = 0
    nombre = ""
    autor = ""
    contenido = ""
    while val < 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1. Ingresar nuevo juego")
        print("2. Ver informacion")
        print("3. Salir")
        val = int(input())
        if val ==1:
            print("Ingrese el nombre del juego")
            nombre = input()
            print("Ingrese el autor del videojuego")
            autor = input()
            print("Ingrese la descripcion del juego")
            contenido = input()
            ingresarJuego(nombre,autor,contenido)
        elif val == 2:
            verDatos()
            input()
        elif val == 3:
            print("adios")