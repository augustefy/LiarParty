# Liar Party 🍻

> Jeu à boire en ligne - basé sur le bluff et la devinette  
> Développé en Django

---

## ✨ Concept

Liar Party est un jeu à boire où chaque joueur partage un fait sur lui-même (vrai ou faux) et les autres doivent deviner.  
Si la majorité se trompe, l'auteur du fait gagne et les autres boivent 🍺.  
Si la majorité a raison, c'est l'auteur qui trinque !

---

## ⚙️ Fonctionnalités principales

✅ Création d'une partie avec un code unique  
✅ Rejoindre une partie par code  
✅ Salle d'attente avant le début  
✅ Rounds :  
   - Soumission du fait par l'auteur  
   - Vote secret des autres joueurs  
   - Révélation du résultat  
✅ Score optionnel  
✅ Tour suivant jusqu'à la fin de la partie  
✅ Interface simple et fun adaptée à l'apéro  

---

## 💻 Stack

- Python 3.12+
- Django 5.x
- TailwindCSS
- SQLite 
- Render.com (comme idée de deploiment )

---

## 🚀 Installation locale

### 1. Cloner le repo
```bash
git clone https://github.com/ton-pseudo/LiarParty.git
cd LiarParty
```

### 2. Créer et activer un environnement virtuel
```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Migrer la base de données
```bash
python manage.py migrate
```

### 5. Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
````


### 6. Lancer le serveur en local (avec Daphne, OBLIGATOIRE pour websockets)
```bash
daphne PartyLiar.asgi:application
```

#### Le jeu sera accessible ici :
#### ➡️ http://127.0.0.1:8000/



