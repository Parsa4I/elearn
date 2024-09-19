from django import forms


class StarsForm(forms.Form):
    CHOICES = [
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
    ]
    rating = forms.ChoiceField(
        label="Rate this course", widget=forms.RadioSelect, choices=CHOICES
    )
