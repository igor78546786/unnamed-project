from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('encontrar-raiz/', views.pagina_encontrar_raiz, name='encontrar_raiz'),
]