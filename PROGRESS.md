# Étapes de Développement (Ubuntu & ROS 2)

Ce journal documente les étapes techniques réalisées dans le terminal Ubuntu 24.04 pour configurer l'environnement ROS 2 Jazzy et mettre en place le système de contrôle gestuel du TurtleBot3.

---

## Étape 1 : Préparation de l'Espace de Travail (Workspace)

Avant de coder, on crée l'architecture du dossier sur Ubuntu.

### Créer les dossiers :
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### Créer le Package ROS 2 :
On définit ici que notre projet s'appelle `gesture_control` et qu'il utilise Python et les messages de navigation.

```bash
ros2 pkg create --build-type ament_python gesture_control --dependencies rclpy geometry_msgs cv_bridge sensor_msgs

```

## Étape 2 : Écriture du Script Python
J'ai utilisé nano pour créer le fichier principal du nœud IA
```bash
nano ~/ros2_ws/src/gesture_control/gesture_control/gesture_controller.py
```

 Le code Python avec YOLOv8 et le lien vers `http://VOTRE_IP:8080/video`. 
Ce script calcule la distance entre votre tête (Blue Dot) et votre main (Green Dot).

### B. La Configuration de l'Exécutable (setup.py)
C'est l'étape que beaucoup oublient. Elle permet à Ubuntu de reconnaître la commande `ros2 run`.

```bash
nano ~/ros2_ws/src/gesture_control/setup.py
```
```bash
cd ~/ros2_ws
colcon build --packages-select gesture_control
source install/setup.bash
```

### C. Les Dépendances (package.xml)
Ce fichier liste les bibliothèques dont le robot a besoin 
```bash
nano ~/ros2_ws/src/gesture_control/package.xml

---


## Étape 3 : Compilation du Projet (Building)


```bash
cd ~/ros2_ws
colcon build --packages-select gesture_control
source install/setup.bash
```

---

## Étape 4 : Lancement du "Corps" (Gazebo & TurtleBot3)

On lance d'abord le robot dans son monde virtuel.

### Ouvrez un nouveau terminal (Terminal 2).


```bash
export TURTLEBOT3_MODEL=burger
source /opt/ros/jazzy/setup.bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Le simulateur s'ouvre et vous voyez le robot "Burger"

---

## Étape 5 : Lancement du "Cerveau" (IA & Pilotage)

On lance maintenant le programme qui regarde votre caméra.

### Ouvrez un nouveau terminal (Terminal 3).


```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run gesture_control gesture_node
```

---

## Étape 6 : Visualisation et Pilotage Réel


###  Fenêtre Vidéo
Une fenêtre apparaît sur l'écran PC montrant ce que le téléphone voit.

###  Inférence
YOLOv8 dessine des cadres autour de nous.

### Pilotage

* **Mettez votre main au centre :** Le robot **Avance**.
* **Mettez votre main à droite :** Le robot **Tourne à Droite**.
* **Mettez votre main à gauche :** Le robot **Tourne à Gauche**.
* **Retirez votre main :** Le robot **s'arrête** (Sécurité).

---