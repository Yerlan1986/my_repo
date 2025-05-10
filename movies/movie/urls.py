from django.urls import path

from movie.views import movies as movies_views
from movie.views import persons as persons_views
from movie.views import comments as comments_views
from movie.views import playlist as playlist_views


urlpatterns = [
    path('list/', movies_views.MovieListAPIView.as_view()),
    path('<int:movie_id>/', movies_views.MovieDetailAPIView.as_view()),
    path('create/', movies_views.MovieCreateAPIView.as_view()),
    path('create/<int:movie_id>/delete/', movies_views.MovieDeleteAPIView.as_view()),
    path('create/<int:movie_id>/update/', movies_views.MovieUpdateAPIView.as_view()),

    path('person/list/', persons_views.PersonListAPIView.as_view()),
    path('create/person/<int:movie_id>/', persons_views.PersonCreateAPIView.as_view()),
    path('person/<int:person_id>/', persons_views.PersonDetailAPIView.as_view()),
    path('person/<int:person_id>/delete/', persons_views.PersonDeleteAPIView.as_view()),
    path('person/<int:person_id>/update/', persons_views.PersonUpdateAPIView.as_view()),

    path('comment/list/<int:movie_id>/', comments_views.CommentListAPIView.as_view()),
    path('create/comment/<int:movie_id>/', comments_views.CommentCreateAPIView.as_view()),
    path('comment/<int:comment_id>/delete/', comments_views.CommentDeleteAPIView.as_view()),
    path('comment/<int:comment_id>/update/', comments_views.CommentUpdateAPIView.as_view()),

    path('playlist/add/<int:movie_id>/', playlist_views.AddToPlaylistAPIView.as_view()),
    path('playlist/delete/<int:movie_id>/', playlist_views.DeleteFromPLaylisAPIView.as_view()),
    path('playlist/list/', playlist_views.PlaylistAPIView.as_view()),

    path('recommendation/list/', playlist_views.GetRecommendationAPIView.as_view()),

]