'''
Created on 23 Nov. 2018

@author: Franklin
'''

from django.urls import path
from restapi.views import (
	UserLoginAPIView,
	UserSignupAPIView,
	list_eventos,
	activar,
)

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(),  name='login'),
    path('signup/', UserSignupAPIView.as_view(),  name='signup'),
    path('evento/list/', list_eventos, name='listaEventos'),
    path('activate/', activar, name='activacion')
    
]