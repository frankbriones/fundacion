from django.urls import path, re_path

from persona import views
from persona.views import talleres_list, personas, signup2, nuevaPersona, edicion, detalle, chart_data, editar_perfil, list_capacitador, inactivar, videos, list_capacitador_inactivos, activar, usuarios_list, delete, editar_perfil_user, contacMail

from django.contrib.auth.decorators import login_required

urlpatterns = [
	

	path(
		route='login/',
		view = views.LoginView.as_view(),
		name = 'login'
	),
	

	path(route = 'logout/', view = views.LogoutView.as_view(), name='logout'),
	path(route = 'lista-users', view = views.usuarios_list, name='usuarios_list'),
	
	path(
        route='perfil/',
        view = views.UpdateProfileView,
        name='update'
    ),
	path('voluntarios/', personas, name='personas'),

	#videos youtube
	path('video-reproducciones/', videos, name='html_video'),


	path('chart-data/voluntarios/', views.chart_data, name='chart_data'),
	path('cambiar-password/', views.change_password, name='change_password'),
	path('nuevo-voluntario/', nuevaPersona, name = 'persona'),
	re_path('detalle-voluntario/(?P<persona_id>\d+)/$', detalle, name = 'detalle'),
	re_path('voluntario-capacitador/inactivar/(?P<persona_id>\d+)/$', inactivar, name = 'persona_inactiva'),
	re_path('capacitador-activar/(?P<persona_id>\d+)/$', activar, name = 'persona_activa'),

	re_path('editar-voluntario/(?P<persona_id>\d+)/$', edicion, name = 'edicion'),
	# path(
 #        route='registro-estudiante/',
 #        view = views.SignupView.as_view(),
 #        name='signup2'
 #    ),
    path(route = 'registro-usuario/', view = signup2,  name='signup2'),

    re_path(route = 'talleres-realizados/(?P<persona_id>\d+)/$', view = talleres_list,  name='talleres_list'),


	re_path('eliminar-usuario/(?P<profile_id>\d+)/', delete, name = 'delete'),
    path('editar', editar_perfil, name = 'editar'),
    re_path('editar-usuario/(?P<profile_id>\d+)/$', editar_perfil_user, name = 'editar_user'),
    path('list-capacitadores/activos', list_capacitador, name='list_capacitador'),
    path('list-capacitadores/inactivos', list_capacitador_inactivos, name='list_capacitador_inactivos'),

    path('notificar-por-correo/', contacMail, name='correo'),
   


]