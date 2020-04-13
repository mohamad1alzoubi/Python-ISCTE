from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


# from . import models


def index(request):
	return HttpResponse("Hello,world. Esta e a pagina de entrada da app votacao.")