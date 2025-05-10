from django.db import models

from django.contrib.auth import get_user_model

from movie.choicesmenu import RoleInMovie, MovieRating

USER = get_user_model()


class Movie(models.Model):
    title = models.CharField(max_length=250)
    year = models.IntegerField()
    released = models.CharField(max_length=250)
    runtime = models.CharField(max_length=250)
    awards = models.CharField(max_length=250)
    poster = models.CharField(max_length=500)
    language = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    average_rating = models.PositiveIntegerField(default=0)
    imdbRating = models.FloatField(null=True, blank=True)

    plot = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    genres = models.ManyToManyField('Genre', through='MovieGenre', related_name='movies')
    persons = models.ManyToManyField('Person', through='PersonRoleInMovie', related_name='movies')

    class Meta:
        unique_together = ("title", "year")

    def __str__(self):
        return f"{self.title} ({self.year})"


class Genre(models.Model):
    genre = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f"({self.id}){self.genre}"


class MovieGenre(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)


class Person(models.Model):
    name = models.CharField(max_length=250, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)


class PersonRoleInMovie(models.Model):
    movie = models.ForeignKey('Movie',
                              on_delete=models.CASCADE,
                              related_name='person_roles'
                              )
    person = models.ForeignKey('Person',
                               on_delete=models.CASCADE,
                               )
    role = models.CharField(
        max_length=15,
        choices=RoleInMovie.choices,
        default=None
    )


class Comment(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=500)
    rating = models.PositiveIntegerField(choices=MovieRating.choices, default=0)

    class Meta:
        unique_together = ("user", "movie")


class UserPlayList(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "movie")


class Recommendation(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.genre} - {self.count}"

    class Meta:
        unique_together = ("user", "genre")






