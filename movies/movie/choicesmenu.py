from django.db import models


class MovieRating(models.IntegerChoices):
    excellent = 5, 'отличный фильм'
    good = 4, 'хороший фильм'
    average = 3, 'средний фильм'
    bad = 2, 'плохой фильм'
    terrable = 1, 'ужасный фильм'


class RoleInMovie(models.TextChoices):
    actor = 'actor', 'Актер'
    director = 'director', 'Режиссер'
    writer = 'writer', 'Сценарист'

