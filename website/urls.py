from django.urls import path, re_path
from website import views 
from website.views import estudiante_t

urlpatterns = [
	path('', views.home, name='inicio'),
	path('conocenos/', views.conocenos, name='conocenos'),
	path('mision-vision-tacitaCaliente/', views.mision, name='mision'),
	path('programas-en-ejecucion/', views.programas, name='programas'),

	# path(
	# 	'visitanos/',
	# 	views.visitanos,
	# 	name='visitanos'
	# 	),

	path('registro-de-voluntario/', views.nuevoVoluntario, name='nuevo_voluntario'),
	path('registro-de-usuario/', views.nuevoEstudiante, name='nuevo_estudiante'),
	re_path('talleres-listado/disponible/', views.TalleresList, name='talleres'),

	re_path('agregar-estudiante/(?P<taller_id>\d+)/$', views.estudiante_t, name='estudiante_t'),
	path('comentario/', views.crear_comentario, name = 'crear_comentario'),
	
]