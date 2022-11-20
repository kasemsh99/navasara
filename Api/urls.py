from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login),


	path('artist/<int:artist_id>/', views.artist_data),
    path('artist/<int:artist_id>/edit/', views.artist_edit),
    path('artist/search/', views.artist_search),
	path('media/search/', views.media_search),
]
