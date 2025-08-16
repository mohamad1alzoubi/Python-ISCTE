from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Questao, Opcao, Voto

def index(request):
    """Página inicial mostrando questões recentes"""
    questoes_recentes = Questao.objects.order_by('-pub_data')[:5]
    context = {
        'questoes_recentes': questoes_recentes,
        'user': request.user,
    }
    return render(request, 'votacao/index.html', context)

def questoes(request):
    """Lista todas as questões"""
    questoes = Questao.objects.order_by('-pub_data')
    context = {
        'questoes': questoes,
        'user': request.user,
    }
    return render(request, 'votacao/questoes.html', context)

def detalhe(request, questao_id):
    """Mostra detalhes de uma questão específica"""
    try:
        questao = Questao.objects.get(pk=questao_id)
    except Questao.DoesNotExist:
        raise Http404("Questão não encontrada")
    
    # Check if user has already voted on this question
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Voto.objects.get(usuario=request.user, opcao__questao=questao)
        except Voto.DoesNotExist:
            pass
    
    context = {
        'questao': questao,
        'user_vote': user_vote,
        'user': request.user,
    }
    return render(request, 'votacao/detalhe.html', context)

@login_required
def votar(request, questao_id):
    """Processa o voto do usuário"""
    questao = get_object_or_404(Questao, pk=questao_id)
    
    try:
        opcao_selecionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        return render(request, 'votacao/detalhe.html', {
            'questao': questao,
            'error_message': "Você não selecionou uma opção válida.",
            'user': request.user,
        })
    
    # Check if user already voted on this question
    existing_vote = Voto.objects.filter(
        usuario=request.user,
        opcao__questao=questao
    ).first()
    
    if existing_vote:
        # Update existing vote
        existing_vote.opcao = opcao_selecionada
        existing_vote.save()
        messages.success(request, 'Seu voto foi atualizado com sucesso!')
    else:
        # Create new vote
        Voto.objects.create(
            usuario=request.user,
            opcao=opcao_selecionada
        )
        messages.success(request, 'Voto registrado com sucesso!')
    
    return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))

@login_required
def resultados(request, questao_id):
    """Mostra resultados de uma questão"""
    questao = get_object_or_404(Questao, pk=questao_id)
    context = {
        'questao': questao,
        'user': request.user,
    }
    return render(request, 'votacao/resultados.html', context)

@login_required
def historico_votos(request):
    """Mostra histórico de votos do usuário"""
    votos = Voto.objects.filter(usuario=request.user).order_by('-data_voto')
    context = {
        'votos': votos,
        'user': request.user,
    }
    return render(request, 'votacao/historico.html', context)

def user_login(request):
    """Processa login do usuário"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', reverse('votacao:index'))
            return redirect(next_url)
        else:
            return render(request, 'votacao/auth/login.html', {
                'error_message': 'Usuário ou senha inválidos.',
            })
    
    return render(request, 'votacao/auth/login.html')

def user_register(request):
    """Processa registro de usuário"""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            return render(request, 'votacao/auth/register.html', {
                'error_message': 'As senhas não coincidem.',
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, 'votacao/auth/register.html', {
                'error_message': 'Este nome de usuário já existe.',
            })
        
        if User.objects.filter(email=email).exists():
            return render(request, 'votacao/auth/register.html', {
                'error_message': 'Este email já está em uso.',
            })
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Auto-login after registration
        login(request, user)
        messages.success(request, 'Conta criada com sucesso!')
        return redirect('votacao:index')
    
    return render(request, 'votacao/auth/register.html')

@login_required
def user_logout(request):
    """Processa logout do usuário"""
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('votacao:index')