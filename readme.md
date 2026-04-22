# Pilotage de Robot ROS 2 par Intelligence Artificielle (YOLOv8)

## Description du Projet
Ce projet permet de piloter un robot simulé (TurtleBot3 Burger) dans **Gazebo** en utilisant la caméra d'un smartphone. Les gestes de l'utilisateur sont analysés en temps réel par **YOLOv8** pour générer des commandes de vitesse (`cmd_vel`).

## Architecture des Fichiers
Voici les fichiers clés de ce projet. Vous pouvez cliquer dessus pour voir le code source :

* **[PROGRESS.md](./PROGRESS.md)** : Journal de bord contenant toutes les commandes Ubuntu (création du workspace, compilation avec colcon).
* **[gesture_controller.py](./src/gesture_control/gesture_control/gesture_controller.py)** : Le script Python principal qui contient l'IA YOLOv8, le traitement d'image et l'envoi des messages ROS 2.
* **[setup.py](./src/gesture_control/setup.py)** : Le fichier de configuration du package ROS 2.

## Fonctionnalités
* **Détection Temps Réel :** Utilisation de YOLOv8 Nano pour une inférence ultra-rapide (<100ms).
* **Contrôle Gestuel :** Algorithme basé sur un vecteur de pointage (tête-main) pour diriger le robot.
* **Architecture ROS 2 :** Compatible avec ROS 2 Jazzy et Gazebo.
* **Optimisation :** Flux vidéo multi-threadé pour éliminer la latence de la caméra vidéo HTTP.

## Technologies Utilisées
* **Middleware :** ROS 2 Jazzy Jalisco
* **IA & Vision :** Ultralytics YOLOv8, OpenCV
* **Simulation :** Gazebo & RViz2
* **Capteur :** IP Webcam (Smartphone Android/iOS)

## Configuration de la Caméra
Avant de lancer le système, assurez-vous de connecter votre téléphone au même réseau Wi-Fi que l'ordinateur. Modifiez ensuite l'adresse IP dans le fichier `gesture_controller.py` :
```python
# Ligne 18 : Modifiez avec l'IP donnée par l'application IP Webcam
self.url = 'http://VOTRE_IP_ICI:8080/video'