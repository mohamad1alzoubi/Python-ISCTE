from rest_framework import serializers
from .models import Questao, Opcao, Voto
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class OpcaoSerializer(serializers.ModelSerializer):
    votos = serializers.ReadOnlyField()
    
    class Meta:
        model = Opcao
        fields = ['id', 'opcao_texto', 'votos']

class QuestaoSerializer(serializers.ModelSerializer):
    opcoes = OpcaoSerializer(many=True, read_only=True)
    total_votos = serializers.ReadOnlyField()
    
    class Meta:
        model = Questao
        fields = ['id', 'questao_texto', 'pub_data', 'opcoes', 'total_votos']

class VotoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    opcao = OpcaoSerializer(read_only=True)
    
    class Meta:
        model = Voto
        fields = ['id', 'usuario', 'opcao', 'data_voto']

class VotoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ['opcao']
    
    def create(self, validated_data):
        user = self.context['request'].user
        opcao = validated_data['opcao']
        
        # Check if user already voted on this option's question
        existing_vote = Voto.objects.filter(
            usuario=user,
            opcao__questao=opcao.questao
        ).first()
        
        if existing_vote:
            # Update existing vote
            existing_vote.opcao = opcao
            existing_vote.save()
            return existing_vote
        else:
            # Create new vote
            return Voto.objects.create(usuario=user, **validated_data)
