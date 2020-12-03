# IoT project

Novembre 2020

* Ayoub Khazzar
* Lucien Burdet
* Marouane Azzouz
* Nassim Khirredine
* Redwan Kara

## Résumé

Le projet d’IOT consiste à mettre en place une application permettant de récupérer les données des capteurs de luminosité et de température.
## Récapitulatif du fonctionnel
  - communication bidirectionnelle
  - messages au format JSON avant d'être chiffrés
  - messages chiffrés avec l'algorithme de vigenere
  - application android et serveur communiquent via **UDP**
  - base de données en **mongodb**
  - paserelle et microbit communiquent en **UART**
  - les micro:bit communiquent entre eux par ondes radio
  - le température et la luminosité s'affichent dans l'ordre donné *par le smartphone* sur *l'écran OLED*

## Sommaire

Nous nous retrouvons avec 4 parties de développement et 1 partie rapport :
- **Rapport :**
  1. [Partie rapport ```rapport_synthetique.docx```](./rapport_synthétique.docx)
- **Développement :**
  2. [Partie Application android : ```android/README.md```](./android/README.md)
  3. [Partie Micro-controlleur écran : ```microBit/README.md```](microBit/README.md) \*
  4. [Partie Micro-controlleur passerelle : ```microBit/README.md```](microBit/README.md) \*
  5. [Partie serveur (ordinateur passerelle) ```server/README.md```](server/README.md)

<small>\* Ce fichier regroupe la partie 3 et 4 </small> 
Nous vous conseillons de lire le [rapport](rapport_synthetique.docx) en premier avant de vous plonger sur les autres éléments de documentation.

*Enfin, tous les codes sont commentés pour faciliter leur compréhension.*
## Tester le projet
- Effectuer les branchements nécessaires
- Lancer les scripts du schéma du rapport (Fig. 1)
- Initialiser la communication entre les micro:bit en appuyant 1 fois sur le ```bouton A``` sur chacun d'eux
- Lancer l'application android