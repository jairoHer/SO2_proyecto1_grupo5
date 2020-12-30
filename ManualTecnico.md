# Manual Técnico Proyecto 1 grupo 5


### Integrantes
| Carnet | Nombre |
| ------ | ------ |
| 201404423 | Jairo Pablo Hernández Guzmán |
| 201504042 | Julio Estuardo Gómez Alonzo  |
| 201503750 | Carlos Eduardo Carías Salan |

## Archivo de Configuración del Despliegue

###NAMESPACE:
La definición del namespace se define en el yml de la configuración de la siguiente manera:
```
apiVersion: v1
kind: Namespace
metadata:
  name: sopes
```
Primero definimos la versión de la API en este caso es la versión: v1, el tipo de del objeto a definir es: Namespace y el nombre de tal objeto es: sopes.


###DEPLOYMENT:
El deployment de uno de los servicios se debe definir de la siguiente manera:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: front
  labels:
    app: proyecto1
  namespace: sopes
spec:
  replicas: 2
  minReadySeconds: 30
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
    type: RollingUpdate 
  selector:
    matchLabels:
      app: proyecto1
  template:
    metadata:
      labels:

        app: proyecto1
    spec:
      containers:
      - name: flask-f
        image: jairinho/cluster_frontend
        ports:
        - containerPort: 5000

```
La metadata para el primer objeto nos dice que el nombre del objeto es front, en el namespace sopes por lo que este objeto estará almacenado en el namespace previamente creado.Para las réplicas definimos 2, para las actualizaciones se definió Rolling Update, y el contenedor tiene como nombre: flask-f y la imagen es la de un cluster que contiene flask y se obtendrá del Docker Hub, se expone el puerto 5000 para este deployment.

###DEPLOYMENT 2:
El deployment de uno de los servicios se debe definir de la siguiente manera:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  labels:
    app: proyecto1
  namespace: sopes
spec:
  replicas: 3
  minReadySeconds: 30
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
    type: RollingUpdate 
  selector:
    matchLabels:
      app: proyecto1
  template:
    metadata:
      labels:
        app: proyecto1
    spec:
      containers:
      - name: flask-b
        image: jairinho/cluster_backend
        ports:
        - containerPort: 5001
```
La metadata para este segundo objeto nos dice que el nombre del objeto es backend, y el namespace de igual manera es sopes por lo que este objeto estará almacenado en el namespace previamente creado.Para las réplicas definimos 3, para las actualizaciones se definió Rolling Update, y el contenedor tiene como nombre: flask-b y la imagen es la de un cluster que contiene flask backend y se obtendrá del Docker Hub, se expone el puerto 5001 para este deployment.


###SERVICIO:
El servicio definido en esta configuración para el loadbalancer se define de la siguiente manera:
```
apiVersion: v1
kind: Service
metadata:
  name: conexión
  namespace: sopes
spec:
  type: LoadBalancer
  ports:
  - name: backend
    protocol: TCP
    port: 5001
    targetPort: 5001
  - name: front
    protocol: TCP
    port: 5000
    targetPort: 5000
  selector:
    app: proyecto1
```
En este objeto que es un servicio el tipo lo definimos como LoadBalancer, para el cual definimos 2 puertos. 
El puerto de nombre backend, le definimos un puerto TCP y el número del puerto 5001, y el target Port 5001. 
El puerto de nombre front, le definimos un puerto TCP y el número del puerto es 5000 y el target port es 5000.

###BASE DE DATOS:
Las bases de datos para esta configuración se definen de la siguiente manera:
```
version: '3'
services:
 mongoso2:
  container_name: mongoso2
  image: mongo
  ports:
   - "27017:27017"
 backend:
  container_name: backend
  build: ./backend
  ports:
   - "5001:5001"
  links:
   - "mongoso2:mongoso2"
  depends_on:
   - mongoso2
 frontend:
  container_name: frontend
  build: ./frontend
  ports:
   - "5000:5000"
  links:
   - "mongoso2:mongoso2"
   - "backend:backend"
  depends_on:
   - mongoso2
   - backend
```

Definimos 2 bases de datos mongo una expuesta en el puerto 5000 y otra en el puerto 5001.


