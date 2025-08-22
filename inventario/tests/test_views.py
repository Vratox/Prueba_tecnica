from decimal import Decimal
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from inventario.models import Producto

@pytest.mark.django_db
class TestInventarioView:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.url = reverse("inventario")  # Asegúrate que en urls.py tengas path(..., name="inventario")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_get_inventario_logged_in(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert "inventario.html" in [t.name for t in response.templates]
        assert "productos" in response.context

    def test_post_valid_producto(self):
        self.client.login(username="testuser", password="12345")
        data = {
            "nombre": "Producto Test",
            "descripcion": "Algo",
            "precio": "100"
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert Producto.objects.filter(nombre="Producto Test").exists()

    def test_post_precio_invalido(self):
        self.client.login(username="testuser", password="12345")
        data = {
            "nombre": "Producto Inválido",
            "descripcion": "Algo",
            "precio": "-50"
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 400
        assert response.json()["status"] == "error"
        assert "precio" in response.json()["errors"]
