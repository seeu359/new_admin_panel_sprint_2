from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import mixins


class Person(mixins.UUIDMixin, mixins.TimeStampMixin):
    full_name = models.CharField(_('full name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Actor')
        verbose_name_plural = _('Actors')


class Genre(mixins.UUIDMixin, mixins.TimeStampMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.CharField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Filmwork(mixins.UUIDMixin, mixins.TimeStampMixin):

    class FilmType(models.TextChoices):
        FILM = 'movie', _('movie')
        TW_SHOW = 'tv_show', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    creation_date = models.DateField(_('date of creation'), null=True, blank=True)

    rating = models.FloatField(_('rating'), blank=True, null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    description = models.CharField(_('description'), null=True, blank=True)
    type = models.CharField(_('type'), choices=FilmType.choices)
    file_path = models.FileField(_('file_path'), blank=True,
                                 null=True, upload_to='app/')
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    person = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Film work')
        verbose_name_plural = _('Film works')


class GenreFilmwork(mixins.UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['genre_id', 'film_work_id'], name='unique_genre_to_film'
            ),
        ]


class PersonFilmwork(mixins.UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='film_person')
    role = models.CharField(max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['film_work_id', 'person_id', 'role'], name='unique_person_film_role',
            )
        ]
