import json
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
# otras importaciones
from .forms import ProductoForm
from .models import Producto
from .serializers import ProductoSerializer

@method_decorator(login_required, name='dispatch')
class inventario_view(View):
    """
    vista para manejar el inventario de productos.
    """
    def get(self, request):
        """
        metodo para obetener la vista del inventario
        """
        form= ProductoForm()
        productos_list = Producto.objects.all().order_by('id')
        paginator = Paginator(productos_list, 10)
        page_number = request.GET.get('page')
        productos = paginator.get_page(page_number)
        return render(request, 'inventario.html', {'form': form, 'productos': productos})
        
    
    def post(self, request, *args, **kwargs):
        try:
            if request.content_type == "application/json":
                datos = json.loads(request.body)
                form = ProductoForm(datos)
            else:
                form = ProductoForm(request.POST)

            if form.is_valid():
                producto = form.save()
                return JsonResponse({'status': 'success', 'id': producto.id}, status=200)
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': {'general': [str(e)]}}, status=500)
        
class api_inventario_view(viewsets.ModelViewSet):
    """
    vista para manejar la API del inventario de productos.
    """
    permission_classes = [IsAuthenticated]

    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

