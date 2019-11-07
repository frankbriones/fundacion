from django.shortcuts import redirect
from django.urls import reverse



class ProfileCompletoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if not request.user.is_anonymous:
            if not request.user.is_staff:
                profile = request.user
                if not profile.imagen or not profile.nombres:
                    if request.path not in [
                    reverse('persona:editar'),
                    reverse('persona:logout'),
                    reverse('website:inicio'),
                    
                    ]:
                        return redirect('persona:editar' )
        
        response = self.get_response(request)
        return response

