from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Search', 'style': 'width: 30% !important'
    }))