from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class PostForm(forms.Form):
        name = forms.CharField(label=('Name'), max_length=50)
        location = forms.CharField(label=('Location'), max_length=100)
        date = forms.DateField(label=('Date (YYYY-MM-DD)'))
        time = forms.TimeField(label=('Time (HH:MM:SS)'))
        host = forms.CharField(label=('Host'), max_length=50)
        rating = forms.IntegerField(label=('Rating'), validators=[MinValueValidator(1),MaxValueValidator(5)])
        description = forms.CharField(label=('Description'), widget=forms.Textarea)