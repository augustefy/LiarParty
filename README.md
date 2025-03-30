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
- TailwindCSS (ou Bootstrap selon préférence)
- PostgreSQL (prod)
- SQLite (dev)
- Whitenoise (pour servir les fichiers statiques)
- Render.com (déploiement recommandé)

---

## 🚀 Installation locale

### 1. Cloner le repo
```bash
git clone https://github.com/ton-pseudo/LiarParty.git
cd LiarParty