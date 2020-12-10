from django.urls import path
from . import views

urlpatterns = [
    path('', views.games),
    path('<int:id>/', views.game),
    path('<int:id>/click/', views.click),
    path('<int:id>/finish/', views.finish),
]