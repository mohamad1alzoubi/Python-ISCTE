from django.urls import path
from . import views

app_name = 'votacao'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('questoes/', views.questoes, name='questoes'),
    path('<int:questao_id>/', views.detalhe, name='detalhe'),
    path('<int:questao_id>/votar/', views.votar, name='votar'),
    path('<int:questao_id>/resultados/', views.resultados, name='resultados'),
    
    # Authentication
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # User features
    path('historico/', views.historico_votos, name='historico'),
]