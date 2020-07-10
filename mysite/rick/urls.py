from django.urls import path

from . import views

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /5/personaje
    path('<int:personaje_id>/personaje', views.personaje, name='personaje'),
    # ex: /5/lugar/
    path('<int:lugar_id>/lugar/', views.lugar, name='lugar'),
    path('<int:capitulo_id>/capitulo/', views.capitulo, name='capitulo'),
    path('<int:lugar_id>/not_found', views.not_found, name = 'not_found'),
    path('search/', views.search, name='search'),
]