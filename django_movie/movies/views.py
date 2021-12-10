from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie
from .forms import ReviewForm


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False) #выводим не помеченные как черновик
    #template_name = 'movies/movie_list.html'


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"
    
    
    


class AddReview(View):
    #Класс для отправки отзывов
    def post(self,request, pk):
        form= ReviewForm(request.POST) #Джанго заполнит форму данными из запроса
        movie = Movie.objects.get(id=pk)
        
        if form.is_valid:
            #остановка сохранения формы, тем самым можно внести изменения в форму
            form=form.save(commit=False) 
            if request.POST.get('parent',None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie= movie #привязка напрямую через объект
            
                 #movie_id - из таблицы многие ко многим (movies_reviews)
            #form.movie_id = pk #присваиваем комментарий по id фильма
            form.save() #добавляем коммент в базу
        return redirect(movie.get_absolute_url())
    
    