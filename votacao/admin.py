from django.contrib import admin
from .models import Questao, Opcao, Voto

# Register your models here.
class OpcaoInline(admin.TabularInline):
    model = Opcao
    extra = 3

class VotoInline(admin.TabularInline):
    model = Voto
    extra = 0
    readonly_fields = ['usuario', 'data_voto']
    can_delete = False

class QuestaoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['questao_texto']}),
        ('Date information', {'fields': ['pub_data'], 'classes': ['collapse']}),
    ]
    inlines = [OpcaoInline]
    list_display = ('questao_texto', 'pub_data', 'foi_publicada_recentemente', 'total_votos')
    list_filter = ['pub_data']
    search_fields = ['questao_texto']
    readonly_fields = ['total_votos']

class OpcaoAdmin(admin.ModelAdmin):
    list_display = ('opcao_texto', 'questao', 'votos')
    list_filter = ['questao']
    search_fields = ['opcao_texto', 'questao__questao_texto']
    readonly_fields = ['votos']
    inlines = [VotoInline]

class VotoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'opcao', 'questao', 'data_voto')
    list_filter = ['data_voto', 'opcao__questao']
    search_fields = ['usuario__username', 'opcao__opcao_texto', 'opcao__questao__questao_texto']
    readonly_fields = ['data_voto']
    
    def questao(self, obj):
        return obj.opcao.questao.questao_texto
    questao.short_description = 'Questão'

admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Opcao, OpcaoAdmin)
admin.site.register(Voto, VotoAdmin)
