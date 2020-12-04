# Documentation serveur

**Le code est commenté pour plus de détails**

## Table des matières
1. Résumé
2. Description

Lancement : ```python3 controller.py```

## 1. Résumé
Le comportement du serveur se trouve dans ```controller.py```. Nous sommes parti du fichier de base proposé dans le *sujet du projet* et l'avons modifié afin de le faire fonctionner dans notre environnement.
Le script ne fonctionne qu'en python3 et il faut le lancer script sur un PC ayant comme OS une distribution *Linux*.

## 2. Description
Le serveur effectue les tâches suivantes.
- Se connecte à la base de donnée **MongoDB**
- Initialise les objets et variables pour **l'UART**
- Prépare et lance un *Thread* pour gérer les connexions UDP avec **l'application android**
- À la réception d'un Thread :
  - On récupère les infos de la connexion 
  - On renvoie les données dans l'UART
- Gère la communication filaire **UART** avec le micro:bit correspondant
- À la réception de données en UART :
  - On converti les données en string
  - Si la string est retry :
    - On renvoie les dernières données envoyées si nécessaire (le micro:bit renvoie "retry\n" en cas d'erreur)
  - Sinon :
    - on enregistre les données dans le fichier texte et la BD
    - on fait parvenir ces données à l'application android

## 3. Installing the server
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