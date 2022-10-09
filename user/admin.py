from django.contrib import admin

# Register your models here.
from .models import (
  Comunidade, Emprestimo, MeuNegocio,
  User, MeuCurso, Curso, Transacao,
  NotaFiscal

)


admin.site.register(User)
admin.site.register(Comunidade)
admin.site.register(Emprestimo)
admin.site.register(MeuCurso)
admin.site.register(Curso)
admin.site.register(MeuNegocio)
admin.site.register(Transacao)
admin.site.register(NotaFiscal)
