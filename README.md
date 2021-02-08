# Projet Edouard
Un bot Discord nommé Edouard :)

Il est fondé sur la bibliothèque en Python [discord.py](https://github.com/Rapptz/discord.py) qui implémente l'API Discord.

## Fonctionnalités
Edouard intègre quelques commandes plus ou moins utiles et intéressantes. Le préfiwe de commande choisi est "?" mais reste facilement modifiable, pour éviter les conflits entre plusieurs bots par exemple.
* ping : le bot renvoie simplement un pong, utile pour vérifier si le bot est en marche ou non sans avoir à regarder dans la liste des personnes du serveur;
* clear : effacer tous les logs du fichier discord.log, utile pendant la phase de développement où l'on teste plein de fois les commandes;
* edt : avec 0 à 2 arguments, elle renvoie un Embed qui affiche l'emploi du temps. Il le récupère sur le site de l'université Lyon 1. Ne mettre aucun argument récupère l'edt du jour même, ùettre un seul argument récupère l'edt de ce jour, mettre deux arguments récupère l'edt sur la période entre les deux dates;
* help : commande de base de Discord.py qui affiche les commandes disponibles;
* todo : gérer une liste de Todo (des tâches à faire) en ajoutant, supprimant, catégorisant les Todo.

Edouard peut aussi répondre à certains messages précis.
* salut : le bot renvoie le message "Bonjour !" accompagné de la mention de l'auteur;
* dm me : le bot envoie un message dans les messages privés de l'auteur.

## Logs
Le bot est prévu pour générer de nombreux logs à chacune de ses actions, de la forme "[date heure]: message", qu'il ajoute dans le fichier discord.log.
Liste des logs générés :
* lors de la connexion/démarrage du bot grâce à la fonction on_ready();
* lors de la réponse à une commande ou un message;
* lors de la capture d'une erreur à cause d'un message, d'une commande ou autre.

## Environnement
Le bot est prévu pour tourner sur le site [Repl.It](https://www.repl.it) grâce à une implementation de Flask. L'application web permet de maintenir le bot allumé même lors de la fermeture de l'onglet.
Il est couplé à un monitoring effectué grâce à [Uptime Robot](https://uptimerobot.com) qui empêche le bot de s'éteindre après une heure sans activité (notamment la nuit).

## Token discord
Le token discord se trouve dans le fichier .env sous la forme d'une variable d'environnement, pour éviter le laisser en clair dans le programme.


#### PS.
J'avoue que je sais pas trop ce que je dis dans ce readme parce que je sais pas ce qu'il faut mettre dedans