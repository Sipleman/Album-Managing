from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class SongForm(forms.Form):
    name = forms.CharField()
    duration = forms.CharField()
    price = forms.CharField()
    id = forms.CharField(widget=forms.HiddenInput())

