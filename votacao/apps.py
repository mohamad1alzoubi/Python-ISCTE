from django.apps import AppConfig


class VotacaoConfig(AppConfig):
    name = 'votacao'
    
    def ready(self):
        import votacao.signals
