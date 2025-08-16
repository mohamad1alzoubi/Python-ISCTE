from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Questao, Opcao, Voto
from .serializers import (
    QuestaoSerializer, OpcaoSerializer, VotoSerializer, 
    VotoCreateSerializer, UserSerializer
)

class QuestaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Questao.objects.all().order_by('-pub_data')
    serializer_class = QuestaoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def resultados(self, request, pk=None):
        questao = self.get_object()
        serializer = self.get_serializer(questao)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recentes(self, request):
        questoes = Questao.objects.order_by('-pub_data')[:5]
        serializer = self.get_serializer(questoes, many=True)
        return Response(serializer.data)

class OpcaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Opcao.objects.all()
    serializer_class = OpcaoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VotoViewSet(viewsets.ModelViewSet):
    serializer_class = VotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Voto.objects.filter(usuario=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VotoCreateSerializer
        return VotoSerializer
    
    @action(detail=False, methods=['get'])
    def historico(self, request):
        votos = self.get_queryset().order_by('-data_voto')
        serializer = self.get_serializer(votos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def votar(self, request):
        serializer = VotoCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            voto = serializer.save()
            return Response({
                'message': 'Voto registrado com sucesso!',
                'voto_id': voto.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def perfil(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
