from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'questoes', api_views.QuestaoViewSet)
router.register(r'opcoes', api_views.OpcaoViewSet)
router.register(r'votos', api_views.VotoViewSet, basename='voto')
router.register(r'usuarios', api_views.UserViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
]
