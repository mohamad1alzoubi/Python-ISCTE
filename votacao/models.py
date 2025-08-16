

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from six import string_types
import datetime 

class Questao(models.Model):
	questao_texto = models.CharField(max_length=200)
	pub_data = models.DateTimeField('data de publicacao')
	
	def __str__(self): 
		return self.questao_texto 
	
	def foi_publicada_recentemente(self):
		return self.pub_data >= timezone.now() - datetime.timedelta(days=1)
	
	def total_votos(self):
		return sum(opcao.votos for opcao in self.opcao_set.all())

class Opcao(models.Model):
	questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
	opcao_texto = models.CharField(max_length=200)
	
	def __str__(self):
		return self.opcao_texto 
	
	@property
	def votos(self):
		return self.voto_set.count()

class Voto(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	opcao = models.ForeignKey(Opcao, on_delete=models.CASCADE)
	data_voto = models.DateTimeField('data do voto', auto_now_add=True)
	
	class Meta:
		unique_together = ['usuario', 'opcao']
		verbose_name = 'Voto'
		verbose_name_plural = 'Votos'
	
	def __str__(self):
		return f'{self.usuario.username} votou em {self.opcao.opcao_texto}' 