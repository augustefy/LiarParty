from django.db import models
import random
import string

# ---------------------------
# UTILS
# ---------------------------

def generate_game_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


# ---------------------------
# MODELES DU JEU
# ---------------------------

# ---- Game ----
class Game(models.Model):
    code = models.CharField(max_length=8, unique=True, default=generate_game_code)
    host = models.ForeignKey('Player', on_delete=models.SET_NULL, null=True, related_name='hosted_games')
    status = models.CharField(max_length=20, default="waiting")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.code}"


# ---- Player ----
class Player(models.Model):
    pseudo = models.CharField(max_length=100)
    game = models.ForeignKey(Game, related_name="players", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True, null=True)  # <-- ajoute null=True

    def __str__(self):
        return self.pseudo


# ---- Round ----
class Round(models.Model):
    game = models.ForeignKey(Game, related_name="rounds", on_delete=models.CASCADE)
    author = models.ForeignKey(Player, on_delete=models.CASCADE)
    statement_text = models.TextField()
    is_true = models.BooleanField()
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Round {self.id} - {self.author.pseudo}"


# ---- Vote ----
class Vote(models.Model):
    round = models.ForeignKey(Round, related_name="votes", on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    guess = models.BooleanField()

    def __str__(self):
        return f"{self.player.pseudo} voted {'True' if self.guess else 'False'}"