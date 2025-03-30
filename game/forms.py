from django import forms
from .models import Player

###### Create Game Form ##########
class CreateGameForm(forms.Form):
    pseudo = forms.CharField(max_length=50, label="Ton pseudo")


###### JOin Form ##########
class JoinGameForm(forms.Form):
    pseudo = forms.CharField(max_length=50, label="Ton pseudo")
    code = forms.CharField(max_length=8, label="Code de la partie")

##### Form of the statement #####
class StatementForm(forms.Form):
    statement_text = forms.CharField(label="Ton bluff", widget=forms.Textarea)
    is_true = forms.BooleanField(label="Coche si c'est vrai", required=False)


#### Form of vote ######
class VoteForm(forms.Form):
    guess = forms.ChoiceField(choices=[(True, 'Vrai'), (False, 'Faux')], widget=forms.RadioSelect, label="Que penses-tu ?")