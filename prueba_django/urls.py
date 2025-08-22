from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
# otras importaciones
from prueba_django.views import login_view, LogoutView
from inventario.views import inventario_view, api_inventario_view

router = routers.DefaultRouter()
router.register(r'productos', api_inventario_view, basename='productos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('inventario/', inventario_view.as_view(), name='inventario'),
    
    
    # api productos
    path('api/', include(router.urls)),

]
