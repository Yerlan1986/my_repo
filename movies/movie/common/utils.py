from rest_framework import serializers


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, name="inline_serializer", data=None, **kwargs):

    serializer_class = create_serializer_class(name=name, fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


class DataTransformation:

    @staticmethod
    def transformation(movie_data: dict) -> dict:
        context_data = {}

        fields = {
            'title': 'Title',
            'year': 'Year',
            'released': 'Released',
            'runtime': 'Runtime',
            'awards': 'Awards',
            'poster': 'Poster',
            'language': 'Language',
            'country': 'Country',
            'genre': 'Genre',
            'plot': 'Plot',
            'imdbRating': 'imdbRating',
            'director': 'Director',
            'writer': 'Writer',
            'actor': 'Actors',
        }

        for key, movie_key in fields.items():
            value = movie_data.get(movie_key)
            context_data[key] = value

        return context_data

    @staticmethod
    def get_values(string: str) -> list:

        values = string.split(',')
        values = map(str.strip, values)

        return list(values)


