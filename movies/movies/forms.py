from django import forms
from django.forms import fields

from .models import Reviews, Rating, RatingStar


# Через post получаем данные по атрибутам, для дальнейшей валидации используют формы

class ReviewForm(forms.ModelForm):
    # Форма отзывов

    class Meta:
        # Указываем от какой модели нужно строить форму
        model = Reviews
        # Указываем поля которые будут в форме
        fields = ("name", "text", "email")


class RatingForm(forms.ModelForm):
    # форма рейтинга

    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)
