# Documentation des micro-controlleurs

***Le code est commenté en anglais pour plus de détails***

## Table des matières
1. Mise en place des 2 micro:bit
  1. Contenu du dossier
  2. Code commun aux deux micro-controlleurs
2. Documentation micro-controlleur passerelle
3. Documentation micro-controlleur relié à l'écran

Lancement : 
- Flasher/lancer ```screen.py``` sur le micro:bit connecté à l'écran OLED
- Flasher/lancer ```uart.py``` sur l'autre micro:bit

## 1. Mise en place des 2 micro:bit

- Pour que les 2 micro:bit puissent communiquer entre eux, il faut lancer les scripts ```screen.py``` et ```uart.py```.
- Appuyer une fois sur le bouton A sur un des micro:bit
  - Cela permet d'initialiser une connexion entre les deux.
- Après cela, ils pourrons s'échanger des données grâce au reste du code dans leur scripts respectifs.
- Pour stoper la connexion il faut appuyer de nouveau sur A sur chacun des micro:bit.

### 1.1. Contenu du dossier 

- Le dossier ```microBit/``` regroupe à la fois le micro-controlleur passerelle et le micro-controlleur qui s'occupe de l'affichage à l'écran.
- ```microBit/libraries/``` est le dossier de *librairies externes* utilisées.
  - ```security.py``` pour le **chiffrement de Vigenere** car :
      * Il ne demande pas beaucoup de ressources
      * Il est facile à mettre en place
      * Il offre une sécurité minimale. 
        * En effet, dans notre cas nous changeons la clé de chiffrement lorsque la communication est établie entre les deux micro:bit.
        * Cette clé est aléatoire.
  - ```ssd1306_text.py``` et ```ssd1306.py``` pour interagir avec l'écran OLED et pouvoir *afficher* des données (utilisé par).
- ```uart.py``` est le code exécuté par le micro-controlleur passerelle
- ```screen.py``` est le code exécuté par le micro-controlleur connecté à l'écran.

### 1.2. Code commun aux deux micro-controlleurs

- Les ***deux micro-controlleurs*** ont le même *protocole de communication* et communiquent entre eux par ondes radio.
- Protocole de communication, variables et fonctions en commun : 
- Protocole :
    - ```init``` : demande de connexion à un autre microbit
      - à la réception d'un ```init``` on génère une nouvelle adresse que l'on envoie à l'autre micro-controlleur pour se synchroniser.
      - On lui envoie un ```accept``` suivi de l'adresse (délimité par ":" )
    - ```accept``` :  synchronise l'adresse des deux micro-controlleur
      - à la réception, on modifie l'adresse du micro:bit et on renvoie la renvoie pour que l'autre fasse de même
      - on utilise également cette adresse comme clé de chiffrement
    - ```stop``` : permet de stopper la connexion entre 2 micro:bit
      - Le micro:bit réinitialise son adresse et sa clé de chiffrement
- Variables :
  - ```com_established``` : boolean pour savoir si une communication a lieue avec un autre micro:bit
  - ```default_address``` : adresse par défaut
- Fonctions :
  - ```send_msg``` : envoie un message chiffré en Vigenere
  - ```listen``` : se met en écoute pour recevoir un message
  - ```manage_protocol``` : gère le protocole de communication en fonction du message reçu

## 2. Documentation micro-controlleur passerelle

- Fichier : ```uart.py```
- Code spécifique dans la boucle while :
  - Écoute sur la communication radio pour l'autre micro:bit.
  - Écoute sur la communication UART.
  - Dès que l'on reçoit sur l'une des deux communications, on envoie le message reçu à l'autre canal de communication
- Si le message reçu provient de l'UART :
  - On vérifie que l'on a bien reçu ```LT``` ou ```TL```.
    - Si c'est le cas, on passe le message à l'autre micro:bit.
      - Tant que le micro:bit n'a pas reçu la réponse du micro-controlleur relié à l'écran, on renvoie, toutes les secondes environ, le message ```LT``` ou ```TL```.
    - Sinon, on demande au serveur de nous renvoyer des données valides.

## 3. Documentation micro-controlleur relié à l'écran

- Fichier : ```screen.py```
- Code spécifique également dans la boucle while :
  - Après avoir initialisé la communication avec l'autre micro:bit et reçu un message, on vérifie le message reçu
    - S'il s'agit de ```LT``` ou ```TL``` :
      -  On affiche dans l'ordre correspondant sur l'écran la température et luminosité
      -  On renvoie à l'autre micro:bit un message au format JSON avec les données que l'on affiche
   
    - sinon on affiche un message d'erreur sur l'écran