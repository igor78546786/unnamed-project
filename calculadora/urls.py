from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('encontrar-raiz/', views.pagina_encontrar_raiz, name='encontrar_raiz'),
    path('sistemas-lineares/', views.pagina_sistemas_lineares, name='sistemas_lineares'),
    path('exportar-relatorio/', views.baixar_relatorio, name='exportar_relatorio'),
    path('salvar-sessao/', views.salvar_sessao, name='salvar_sessao'),
    path('historico/', views.pagina_historico, name='historico'),
    path('carregar/<int:sessao_id>/', views.carregar_sessao, name='carregar_sessao'),
]