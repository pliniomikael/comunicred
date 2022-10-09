from django.http import JsonResponse

# Create your views here.
from .models import User, Comunidade, Emprestimo

def home(request):

  aa = User.objects.first()
  # nota_month = {
  #   'mes': 10,
  #   'ano': 2022
  # }
  nota_month = None

  return JsonResponse({'data': aa.to_dict(nota_months=nota_month)})
