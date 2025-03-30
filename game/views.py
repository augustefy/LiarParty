from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Game, Player, Round, Vote
from .forms import CreateGameForm, JoinGameForm, StatementForm, VoteForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.views.decorators.http import require_POST


# CREATE GAME
def create_game(request):
    if request.method == "POST":
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game = Game.objects.create()
            player = Player.objects.create(pseudo=form.cleaned_data["pseudo"], game=game)
            game.host = player
            game.save()
            request.session["player_id"] = player.id

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"lobby_{game.code}",
                {"type": "player_update"}
            )

            return redirect("lobby", code=game.code)
    else:
        form = CreateGameForm()
    return render(request, "game/create_game.html", {"form": form})

# JOIN GAME
def join_game(request):
    if request.method == "POST":
        form = JoinGameForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"].upper()
            pseudo = form.cleaned_data["pseudo"]
            game = get_object_or_404(Game, code=code, status="waiting")
            player = Player.objects.create(pseudo=pseudo, game=game)
            request.session["player_id"] = player.id

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"lobby_{game.code}",
                {"type": "player_update"}
            )

            return redirect("lobby", code=game.code)
    else:
        form = JoinGameForm()
    return render(request, "game/join_game.html", {"form": form})


# LOBBY
def lobby(request, code):
    game = get_object_or_404(Game, code=code)
    players = game.players.all()
    player_id = request.session.get("player_id")
    return render(request, "game/lobby.html", {"game": game, "players": players, "player_id": player_id})


# START GAME
def start_game(request, code):
    game = get_object_or_404(Game, code=code)
    player_id = request.session.get("player_id")
    if game.host.id != player_id:
        return HttpResponse("Non non non josé ol del paso josé!")

    game.status = "started"
    game.save()

    # Notify WS
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"lobby_{game.code}",
        {"type": "game_started"}
    )

    return redirect("submit_statement", code=game.code)


# SUBMIT STATEMENT
def submit_statement(request, code):
    game = get_object_or_404(Game, code=code)
    player = get_object_or_404(Player, id=request.session.get('player_id'))
    if not player == game.host:
        return HttpResponse("L'hôte commence toujours !")

    if request.method == "POST":
        form = StatementForm(request.POST)
        if form.is_valid():
            round = Round.objects.create(
                game=game,
                author=player,
                statement_text=form.cleaned_data['statement_text'],
                is_true=form.cleaned_data['is_true']
            )
            return redirect("vote", code=game.code, round_id=round.id)
    else:
        form = StatementForm()

    return render(request, "game/submit_statement.html", {"form": form, "game": game})


# VOTE
def vote(request, code, round_id):
    game = get_object_or_404(Game, code=code)
    round = get_object_or_404(Round, id=round_id)
    player = get_object_or_404(Player, id=request.session.get('player_id'))

    if player == round.author:
        return render(request, "game/waiting_votes.html", {"game": game, "round": round})

    if Vote.objects.filter(round=round, player=player).exists():
        return render(request, "game/waiting_votes.html", {"game": game, "round": round})

    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            Vote.objects.create(
                round=round,
                player=player,
                guess=form.cleaned_data['guess'] == "True"
            )
            return render(request, "game/waiting_votes.html", {"game": game, "round": round})
    else:
        form = VoteForm()

    return render(request, "game/vote.html", {"form": form, "game": game, "round": round})


# ROUND RESULT
def round_result(request, code, round_id):
    game = get_object_or_404(Game, code=code)
    round = get_object_or_404(Round, id=round_id)

    votes = round.votes.all()
    total = votes.count()
    true_votes = votes.filter(guess=True).count()
    false_votes = total - true_votes

    majority = True if true_votes > false_votes else False
    success = (majority != round.is_true)

    round.is_finished = True
    round.save()

    return render(request, "game/round_result.html", {
        "game": game,
        "round": round,
        "votes": votes,
        "success": success,
        "true_votes": true_votes,
        "false_votes": false_votes
    })