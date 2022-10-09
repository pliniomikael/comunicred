from django.http import JsonResponse

# Create your views here.
from .models import Cliente

def home(request):

  data = []
  clientes = Cliente.objects.all().exclude(user__is_staff=True)
  for cliente in clientes:
    data.append(cliente.to_dict())


  return JsonResponse({'data': data})
