from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Category, Movie, Actor, Genre, Reviews, Rating
from .forms import ReviewForm, RatingForm


class GenreYear():
    # Жанры и года выхода фильма

    def get_genres(self):
        return Genre.objects.all()

    # def get_rating(self):
    #     return Rating.objects.all().order_by('-star')

    def get_years(self):
        return Movie.objects.order_by('-year').values('year')[:5]  # забираем только года


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)  # выводим не помеченные как черновик
    # template_name = 'movies/movie_list.html'


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm
        return context


class AddReview(View):
    # Класс для отправки отзывов
    def post(self, request, pk):
        form = ReviewForm(request.POST)  # Джанго заполнит форму данными из запроса
        movie = Movie.objects.get(id=pk)
        review = Reviews.objects.filter(movie=movie)

        if request.POST:

            if '__drop' in request.POST:
                Reviews.delete(review)
            else:

                if form.is_valid:
                    # остановка сохранения формы, тем самым можно внести изменения в форму
                    form = form.save(commit=False)
                    if request.POST.get('parent', None):
                        form.parent_id = int(request.POST.get("parent"))
                    form.movie = movie  # привязка напрямую через объект

                    # movie_id - из таблицы многие ко многим (movies_reviews)
                    # form.movie_id = pk #присваиваем комментарий по id фильма
                    form.save()  # добавляем коммент в базу
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    # Информация об актере
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    # Фильтрация фильмов
    def get_queryset(self):
        # вытаскиваем список из get запроса и фильтруем по нему movie
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset


class Search(ListView):
    # поиск по названию
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))
        # __icontains - не учитывает регистр

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")  # для работоспособности пагинации
        return context


class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        movie = Movie.objects.get(pk=int(request.POST.get('movie')))
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                # ip='127.00.00',
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),  # скрытое поле
                defaults={
                    'star_id': int(request.POST.get('star'))  # замена
                }

            )
            return redirect(movie.get_absolute_url())

        return redirect('home')


class show_rating_movies(ListView):
    def get_queryset(self, request):
        rating = Rating.objects.filter(star=self.request.GET)
        return rating.movie__set.all()
