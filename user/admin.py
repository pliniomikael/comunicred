from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
# Register your models here.
from .models import (
  Comunidade, Emprestimo, MeuNegocio,
  Cliente, MeuCurso, Curso, Transacao,
  NotaFiscal

)


class ComunidadeInline(admin.TabularInline):
    model = Comunidade
    extra = 0

class EmprestimoInline(admin.TabularInline):
    model = Emprestimo
    extra = 0

class MeuNegocioInline(admin.TabularInline):
    model = MeuNegocio
    extra = 0

class TransacaoInline(admin.TabularInline):
    model = Transacao
    extra = 0

class NotaFiscalInline(admin.TabularInline):
    model = NotaFiscal
    extra = 0


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'telefone', 'moedas', 'comunidade', 'status', 'map_link')
    list_filter = ('status',)
    search_fields = ['cpf']

    ordering = ('-id', )
    inlines = [MeuNegocioInline, EmprestimoInline, NotaFiscalInline]

    def map_link(self, obj):
        link = "%s,%s" % (obj.latitude, obj.longitude)
        return format_html("<a href='https://www.google.com.br/maps/@{url},13z' target='_blank'>Olhar no Maps</a>", url=link)
    map_link.short_description = 'Map'


class ComunidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'count_user', 'count_user_moedas',)
    list_filter = ('nome',)
    search_fields = ['nome',]

    ordering = ('-id', )
    # inlines = [UserInline,]

    def count_user(self, obj):
      return Cliente.objects.filter(comunidade__nome=obj.nome).count()
    count_user.short_description = 'Clientes na Comunidade'

    def count_user_moedas(self, obj):
      total = Cliente.objects.filter(comunidade__nome=obj.nome).aggregate(Sum('moedas'))
      return total['moedas__sum']
    count_user_moedas.short_description = 'Total de Moedas na Comunidade'


class EmprestimoAdmin(admin.ModelAdmin):
    list_display = (
      'user', 'valor', 'parcelas',
      'quantas_pagas', 'valor_parcela',
      'credito_disponivel', 'data_criação', 'finalizado',)
    list_filter = ('user',)
    search_fields = ['user',]

    ordering = ('-id', )


class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = (
      'user', 'nome_estabelecimento', 'valor',
      'data_geracao', )
    list_filter = ('user',)
    search_fields = ['user',]

    ordering = ('-id', )

class TransacaoAdmin(admin.ModelAdmin):
    list_display = (
      'negocio', 'valor', 'tipo', 'descricao',
      'criada_em', )
    list_filter = ('negocio',)
    search_fields = ['negocio',]

    ordering = ('-id', )


class MeuNegocioAdmin(admin.ModelAdmin):
    list_display = (
      'user', 'nome', 'total_entrada', 'total_saida',
      'saldo', )
    list_filter = ('user',)
    search_fields = ['user',]

    ordering = ('-id', )

# admin.site.register(User, UserAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Comunidade, ComunidadeAdmin)
admin.site.register(Emprestimo, EmprestimoAdmin)
admin.site.register(MeuCurso)
admin.site.register(Curso)
admin.site.register(MeuNegocio, MeuNegocioAdmin)
admin.site.register(Transacao, TransacaoAdmin)
admin.site.register(NotaFiscal, NotaFiscalAdmin)
