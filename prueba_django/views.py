from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

class login_view(View):
    """
    vista para manejar el login de la aplicación.
    """
    def get(self, request):
        """
        metodo para obtener la vista del login
        """
        return render(request, 'login.html')
    
    def post(self, request):
        """
        metodo para procesar el formulario de login
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inventario')
        else:
            return render(request, 'login.html', {'form': {'errors': True}})
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login_view')