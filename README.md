# Flyers Amiens - Distribution de tracts 

## Objectif du projet ?

C'est une application web qui permet de **suivre la distribution de flyers dans les rues d'Amiens**. 

Imaginez que vous avez plusieurs personnes qui distribuent des flyers dans différentes rues de la ville. Cette application vous permet de :
-  Savoir exactement quelles rues ont déjà été faites
-  Éviter que deux personnes fassent la même rue
-  Voir en temps réel sur une carte où en est la distribution
-  Donner accès uniquement aux personnes autorisées

## Comment ça marche ?

### Pour les distributeurs
1. Ils reçoivent un **code d'accès unique** (comme un mot de passe)
2. Ils ouvrent l'application sur leur téléphone
3. Ils voient une carte avec toutes les rues d'Amiens
4. Quand ils terminent une rue, ils cliquent dessus → elle devient verte
5. Les autres distributeurs voient immédiatement cette mise à jour

### Pour l'administrateur
- Vous générez les codes d'accès pour vos distributeurs avec le script Python
- Vous pouvez voir qui a distribué quoi
- Vous pouvez réinitialiser les données si besoin

## Les fichiers du projet

- **`index.html`** : L'application principale (la carte interactive)
- **`generate_ids.py`** : Le script pour créer/gérer les codes d'accès
- **`authorized_ids.json`** : La liste des codes d'accès valides

## Utilisation simple

### Donner accès à un nouveau distributeur
```bash
python generate_ids.py generate Emmanuel
```
→ Cela génère un code unique pour "Emmanuel" que vous lui donnez

### Voir tous les codes créés
```bash
python generate_ids.py list
```

### Ouvrir l'application
Avec le lien de l'application, vous pouvez l'ouvrir dans votre navigateur web

## Sécurité

- Seul l'administrateur a accès au fichier `generate_ids.py`
- Chaque distributeur reçoit un code unique et personnel
- Les données sont synchronisées en temps réel via Firebase (cloud sécurisé)
- Impossible de deviner les codes d'accès (cryptés)

## En résumé

C'est comme Google Maps + un système de "fait/pas fait" pour organiser efficacement la distribution de flyers dans toute une ville ! 

