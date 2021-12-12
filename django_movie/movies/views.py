from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Category, Movie, Actor
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
    
    #Модуль для отображения категорий - для предотвращения дублирования кода помещен в 
    # templatetags
   # def get_context_data(self, *args, **kwargs):
    #    context = super().get_context_data(*args, **kwargs) #вызывается метод родителя (ListView)
     #   context["categories"] = Category.objects.all() #добавляем в словарь значения по ключу
      #  return context
    
    
    


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
    
    
    
class ActorView(DetailView):
    #Информация об актере
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name" 
    
    