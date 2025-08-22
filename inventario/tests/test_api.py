from decimal import Decimal
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from inventario.models import Producto

@pytest.mark.django_db
class TestApiInventarioView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="apiuser", password="12345")
        self.client.force_authenticate(user=self.user)
        self.url = "/api/productos/"  # Ajusta a tu urls.py

    def test_list_productos(self):
        Producto.objects.create(nombre="Prod 1", descripcion="Desc", precio=10)
        Producto.objects.create(nombre="Prod 2", descripcion="Desc", precio=20)

        response = self.client.get(self.url)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_create_producto(self):
        data = {
            "nombre": "Nuevo API",
            "descripcion": "Creado por API",
            "precio": Decimal("150")
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == 201
        assert Producto.objects.filter(nombre="Nuevo API").exists()

    def test_update_producto(self):
        producto = Producto.objects.create(nombre="Viejo", descripcion="x", precio=10)
        url_detalle = f"{self.url}{producto.id}/"
        data = {"nombre": "Actualizado", "descripcion": "y", "precio": 200}
        response = self.client.put(url_detalle, data, format="json")
        assert response.status_code == 200
        producto.refresh_from_db()
        assert producto.nombre == "Actualizado"

    def test_delete_producto(self):
        producto = Producto.objects.create(nombre="Eliminar", descripcion="x", precio=10)
        url_detalle = f"{self.url}{producto.id}/"
        response = self.client.delete(url_detalle)
        assert response.status_code == 204
        assert not Producto.objects.filter(id=producto.id).exists()
