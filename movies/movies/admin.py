from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews



@admin.register(Category) # = #admin.site.register(Category, CategoryAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name", "url"] #Так выстроится таблица в админке
    list_display_links = ["name"] #Имя поля, которое будет являться ссылкой на запись в БД 
    
    
class ReviewInline(admin.StackedInline): #все отзывы на фильм
    model = Reviews
    extra = 1 #кол-во дополнительных полей отзывов на фильм в админке
    readonly_fields = ["name", "email"]
     
@admin.register(Movie)  
class MovieAdmib(admin.ModelAdmin):
    list_display = ["title", "category","url", "draft"]
    list_filter = ["category","year"] #фильтрация
    search_fields =  ["title", "category__name"] #поиск по атрибутам
    inlines = [ReviewInline]  #только для m2m / foreign key
    save_on_top = True #сохранение сверху страницы
    save_as = True
    list_editable = ["draft"] #редактирование атрибута прям из меню
    fieldsets = ( #Разделение атрибутов по группам
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster","trailer")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    


@admin.register(Reviews)    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "parent", "movie", "id"]
    readonly_fields = ["name", "email"] # поля которые не редактируются
    
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image", )
    
    #Метод, выводящий image в админке
    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="50", height="60" ')

    get_image.short_description = "Изображение"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip", "star")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie","get_image")
    
    readonly_fields = ("get_image", )
    
    #Метод, выводящий image в админке
    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="50", height="60" ')

    get_image.short_description = "Изображение"
    
    

# Register your models here.
#admin.site.register(Category, CategoryAdmin)
#admin.site.register(Genre)
#admin.site.register(Movie)
#admin.site.register(MovieShots)
#admin.site.register(Actor)
#admin.site.register(Rating)
admin.site.register(RatingStar)
#admin.site.register(Reviews)

