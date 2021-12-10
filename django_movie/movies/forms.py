from django import forms
from django.forms import fields

from .models import Reviews 

#Через post получаем данные по атрибутам, для дальнейшей валидации используют формы

class ReviewForm(forms.ModelForm):
    #Форма отзывов
    
    
    class Meta:
        #Указываем от какой модели нужно строить форму
        model = Reviews
        #Указываем поля которые будут в форме
        fields= ("name", "text", "email")