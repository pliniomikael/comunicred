import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
from django.contrib import admin

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.db import models


class Cliente(models.Model):
	user = models.OneToOneField(User, verbose_name=_("Cliente"), related_name='cliente', on_delete=models.CASCADE)
	cpf = models.CharField(_("CPF"), max_length=15, unique=True)
	cidade = models.CharField(_("Cidade"), max_length=50, null=True, blank=True)
	telefone = models.CharField(_("Telefone"), max_length=50, null=True, blank=True)
	latitude = models.CharField(_("Latitude"), max_length=50, null=True, blank=True)
	longitude = models.CharField(_("Longitude"), max_length=50, null=True, blank=True)
	moedas = models.IntegerField(_("Moedinhas"), default=0)
	comunidade = models.ForeignKey(
		"user.Comunidade", verbose_name=_("Comunidade"), related_name="usuarios",
	null=True, blank=True, on_delete=models.CASCADE
	)
	status = models.BooleanField(_("Ativado/Desativado"), default=False)

	class Meta:
		verbose_name = "Cliente"
		verbose_name_plural = "Clientes"

	def __str__(self):
		return self.user.get_full_name()

	def to_dict(self, nota_months=None):
		integrantes = Cliente.objects.filter(comunidade=self.comunidade).order_by('-moedas')
		if nota_months:
			notas = [nota.to_dict() for nota in self.notas_fiscais.filter(data_geracao__month=nota_months['mes'], data_geracao__year=nota_months['ano'],)]
		else:
			notas = [nota.to_dict() for nota in self.notas_fiscais.all()]
		return {
			'id': self.id,
			'fullname': self.user.get_full_name(),
			'cpf': self.cpf,
			'moedas': self.moedas,
			'notas': notas,
			'comunidade': {
				'nome': self.comunidade.nome,
				'integrantes': [{'id': pessoa.id, 'nome': pessoa.user.get_full_name(), 'moedas': pessoa.moedas} for pessoa in integrantes],
			},
			'emprestimos': [emprestimo.to_dict() for emprestimo in self.emprestimos.all()],
			'meus_cursos': [curso.to_dict() for curso in self.cursos.all()],
			'meu_negocio': [negocio.to_dict() for negocio in self.negocios.all()],

		}

class Comunidade(models.Model):

	nome = models.CharField(_("Nome da Comunidade"), max_length=50)

	class Meta:
		verbose_name = _("Comunidade")
		verbose_name_plural = _("Comunidades")

	def __str__(self):
		return self.nome

class Emprestimo(models.Model):
	user = models.ForeignKey(
		Cliente, verbose_name=_("Colaborador"), related_name="emprestimos",
		related_query_name="emprestimo", on_delete=models.CASCADE)
	valor = models.DecimalField(_("Valor Empréstimo"), max_digits=9, decimal_places=2)
	parcelas = models.IntegerField(_("Parcelas"))
	quantas_pagas = models.IntegerField(_("Quantas pagas"), null=True, blank=True)
	finalizado = models.BooleanField(_("Finalizado"), default=False)
	data_criação = models.DateField(_("Data de Criação do Empréstimo"), auto_now=False, auto_now_add=False)

	@property
	@admin.display(description='Valor Parcelas')
	def valor_parcela(self):
		return float('%.2f' % (self.valor/self.parcelas))

	@property
	@admin.display(description='Crédito Dispónivel')
	def credito_disponivel(self):
		return self.quantas_pagas * self.valor_parcela

	@property
	def credito_utilizado(self):
		return self.faltam * self.valor_parcela

	@property
	def faltam(self):
		return self.parcelas - self.quantas_pagas

	@property
	def proximas_parcelas(self):
		faltam_parcelas = []
		if self.quantas_pagas > 0:
			mes_atual = self.data_criação + relativedelta(months=self.quantas_pagas)
		else:
			mes_atual = self.data_criação

		for mes in range(1, self.faltam):
			obj = {
				"mes": (mes_atual + relativedelta(months=mes)).strftime("%A %d. de %B %Y").title(),
				"valor": float(self.valor_parcela)
			}
			faltam_parcelas.append(obj)
		return faltam_parcelas

	def to_dict(self):
		return {
            'id': self.id,
            'valor': float('%.2f' % (self.valor)),
            'parcelas': int(self.parcelas),
            'quantas_pagas': int(self.quantas_pagas),
			'credito_utilizado': float('%.2f' % self.credito_utilizado),
			'credito_disponivel': float('%.2f' % self.credito_disponivel),
            'data_criação': self.data_criação,
            'valor_parcela': float('%.2f' % self.valor_parcela),
            'proximas_parcelas': self.proximas_parcelas,
            'finalizado': self.finalizado,
        }

	class Meta:
		verbose_name = _("Empréstimo")
		verbose_name_plural = _("Empréstimos")

	def __str__(self):
		return self.user.user.get_full_name()

CURSO_STATUS_CHOICES = (
	('FINALIZADO', 'Finalizado'), ('DISPONIVEL', 'Disponivel'), ('ANDAMENTO', 'Em Andamento'),
)
class MeuCurso(models.Model):

	user = models.ForeignKey(Cliente, verbose_name=_("Usuario"), related_name="cursos",
		related_query_name="curso", on_delete=models.CASCADE
	)
	curso = models.ForeignKey("user.Curso", verbose_name=_("Meus Cursos"), on_delete=models.CASCADE)
	status = models.CharField(_("Status"), choices=CURSO_STATUS_CHOICES, max_length=15)

	class Meta:
		verbose_name = _("Meu Curso")
		verbose_name_plural = _("Meus Cursos")

	def __str__(self):
		return self.curso.nome

	def to_dict(self):
		return {
			'id': self.curso.id,
			'nome': self.curso.nome,
			'capa': self.curso.image.url,
			'status': self.status
		}


class Curso(models.Model):

	nome = models.CharField(_("Curso"), max_length=50)
	duracao = models.TimeField(_("Duração"), auto_now=False, auto_now_add=False)
	image = models.ImageField(_("Capa"), blank=True, null=True)
	status = models.BooleanField(_("Ativado/Desativado"), default=False)

	class Meta:
		verbose_name = _("curso")
		verbose_name_plural = _("cursos")

	def __str__(self):
		return self.nome


class MeuNegocio(models.Model):
	user = models.ForeignKey(Cliente, verbose_name=_("Meu Negocio"), related_name="negocios",
		related_query_name="negocio", on_delete=models.CASCADE)
	nome = models.CharField(_("Nome"), max_length=50)

	@property
	@admin.display(description='Saldo')
	def saldo(self):
		return float('%.2f' % (self.total_entrada - self.total_saida))

	@property
	@admin.display(description='Total Entradas')
	def total_entrada(self):
		total = 0
		for item in self.transacoes.filter(tipo='ENTRADA'):
			total += item.valor
		return float('%.2f' % total)

	@property
	@admin.display(description='Total Saída')
	def total_saida(self):
		total = 0
		for item in self.transacoes.filter(tipo='SAIDA'):
			total += item.valor
		return float('%.2f' % total)

	class Meta:
		verbose_name = _("Meu Negocio")
		verbose_name_plural = _("Meus Negocios")

	def to_dict(self):
		return {
			'id': self.id,
			'nome': self.nome,
			'saldo': self.saldo,
			'total_saida': self.total_saida,
			'total_entrada': self.total_entrada,
			'transacoes': [
				{'saida': [{'id': saida.id, 'valor': float('%.2f' % saida.valor), 'descricao': saida.descricao, 'data_criada': saida.criada_em} for saida in self.transacoes.filter(tipo='SAIDA')]},
				{'entrada': [{'id': entrada.id, 'valor': float('%.2f' % entrada.valor), 'descricao': entrada.descricao, 'data_criada': entrada.criada_em} for entrada in self.transacoes.filter(tipo='ENTRADA')]},
			],
		}
	def __str__(self):
		return self.nome

TRANSACAO_STATUS_CHOICES = (
	('ENTRADA', 'Entrada'), ('SAIDA', 'Saida'),
)
class Transacao(models.Model):
	negocio = models.ForeignKey(MeuNegocio, verbose_name=_("Negocio"), related_name="transacoes",
		related_query_name="transacao", on_delete=models.CASCADE)
	valor = models.DecimalField(_("Valor"), max_digits=9, decimal_places=2)
	criada_em = models.DateTimeField(_("Criada Em"), auto_now=False, auto_now_add=False)
	tipo = models.CharField(_("Tipo"), choices=TRANSACAO_STATUS_CHOICES, max_length=50)
	descricao = models.CharField(_("Descricao"), max_length=50, null=True, blank=True)

	class Meta:
		verbose_name = _("Transação")
		verbose_name_plural = _("Transações")

	def __str__(self):
		return ("%s - %s - %s" % (self.negocio.nome, self.valor, self.tipo))


class NotaFiscal(models.Model):
	user = models.ForeignKey(Cliente, verbose_name=_("Usuario"), related_name="notas_fiscais",
		related_query_name="nota_fiscal", on_delete=models.CASCADE)
	nome_estabelecimento = models.CharField(_("Nome do Estabelecimento"), max_length=50)
	numero_nota = models.CharField(_("Numero da Nota"), max_length=50)
	valor = models.DecimalField(_("Valor"), max_digits=9, decimal_places=2)
	data_geracao = models.DateTimeField(_("Data Geração"), auto_now=False, auto_now_add=False)
	url = models.URLField(_("Url"), max_length=500)

	class Meta:
		verbose_name = _("Nota Fiscal")
		verbose_name_plural = _("Notas Fiscais")

	def __str__(self):
		return self.nome_estabelecimento

	def to_dict(self):
		return {
			'numero_nota': self.numero_nota,
			'nome_estabelecimento': self.nome_estabelecimento,
			'valor': float('%.2f' % self.valor),
			'data_geracao': self.data_geracao,
		}
