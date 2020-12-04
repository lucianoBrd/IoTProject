# Documentation Android

- Vous trouverez des **commentaires en anglais** en navigant dans le **code**

## Table des matières
1. Installation
2. Introduction
3. Contenu

## 1. Installation
Deux options : 
- Lancer le fichier ```IoTApp.apk``` sur un appareil android
- Ouvrir le dossier ```android/IoTApp/``` dans ***Android Studio*** et lancer un émulateur

## 2. Introduction
Le dossier ```android/``` contient la partie android du projet d'IoT. Voici un aperçu de l'application :
![capture-appli](Capture.png "capture appli")

## 3. Contenu
1. Code source de l'application ```android/IoTApp/``` avec notamment ***quelques fichiers importants*** :
  - 2 classes java :
    - MainActivity.java
      - Classe principal de l'application, gère la connexion à la passerelle
      - Contient un Thread qui permet de recevoir des données en UDP
    - Send.java (AsyncTask)
      - Classe servant à envoyer des données en UDP
    - Cette séparation en AsyncTask et Thread permet d'éviter que l'exécution de ces morceaux de code **ne bloquent** l'application.
  - 1 fichier xml :
    - res/layout/activity_main.xml
      - Contient le layout de l'application (boutons, inputs, ...). Le bouton envoyer permet d'envoyer ```LT``` ou ```TL``` au serveur. Le bouton est désactivé jusqu'à ce que l'application reçoive une réponse du serveur.


2. Fichier d'installation android ```android/IoTApp.apk```
