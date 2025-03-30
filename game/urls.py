from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_game, name='create_game'),
    path('join/', views.join_game, name='join_game'),
    path('game/<str:code>/', views.lobby, name='lobby'),
    path('game/<str:code>/start/', views.start_game, name='start_game'),
    path('game/<str:code>/statement/', views.submit_statement, name='submit_statement'),
    path('game/<str:code>/round/<int:round_id>/vote/', views.vote, name='vote'),
    path('game/<str:code>/round/<int:round_id>/result/', views.round_result, name='round_result'),
    path("game/<str:code>/waiting/", views.waiting_statement, name="waiting_statement"),
]