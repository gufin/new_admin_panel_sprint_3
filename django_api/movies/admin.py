from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name', 'description', 'id')
    list_filter = (('created', DateFieldListFilter),
                   ('modified', DateFieldListFilter),)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ('film_work', 'person',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        'title', 'type', 'creation_date', 'rating', 'get_genres',
        'get_directors', 'created', 'modified')
    list_prefetch_related = ['genres', 'persons']

    list_filter = ('type', 'creation_date')

    search_fields = ('title', 'description', 'id')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            *self.list_prefetch_related)

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    def get_directors(self, obj):
        return ', '.join([person.full_name for person in
                          obj.persons.filter(personfilmwork__role='director')])

    get_genres.short_description = _('Жанры фильма')
    get_directors.short_description = _('Режиссеры')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    list_display = ('full_name', 'created', 'modified')
    list_filter = (('created', DateFieldListFilter),
                   ('modified', DateFieldListFilter),)
    search_fields = ('full_name', 'id')
