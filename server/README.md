# Documentation serveur

**Le code est commenté pour plus de détails**

## Table des matières
1. Résumé
2. Description
3. Installing the server

Lancement : ```python3 controller.py```

## 1. Résumé
Le comportement du serveur se trouve dans ```controller.py```. Nous sommes parti du fichier de base proposé dans le *sujet du projet* et l'avons modifié afin de le faire fonctionner dans notre environnement.
Le script ne fonctionne qu'en python3 et il faut le lancer script sur un PC ayant comme OS une distribution *Linux*.

## 2. Description
Le serveur effectue les tâches suivantes.
- Se connecte à la base de donnée **MongoDB**
- Initialise les objets et variables pour **l'UART**
- Prépare et lance un *Thread* pour gérer les connexions UDP avec **l'application android**
- Gère la communication filaire **UART** avec le micro:bit correspondant
- 
## 3. Installing the server
In a new raspbian installation:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git python python-serial minicom
sudo usermod -aG dialout pi
```

Add a line into `rc.local`to start the game

For the db : 

in one term
```
docker pull mongo
docker rm mongodb
docker run --name mongodb -p 27017:27017 mongo
```

in another one
```
docker exec -it mongodb bash #to acceed to mongo 
mongo
use admin
db.createUser({
  user: "admin", 
  pwd: "secure", 
  roles: [ { role: "root", db: "admin" } ]
})
db.createCollection('iot')
```
