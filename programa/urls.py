from django.urls import path, re_path
from programa import views
from programa.views import inactivar_evento

urlpatterns = [

	#API
	path('list/', views.list_programas, name='programas'),
	
	
	path('lista-eventos', views.programa, name = 'programas'),
	path('registro-evento', view = views.nuevoPrograma, name = 'programa'),

	path('programa-nuevo/', view = views.nuevoEvento, name = 'evento'),
	re_path('detalle-programa/(?P<programa_id>\d+)/$', views.editaPrograma, name = 'edita'),
	re_path('agreagar-producto/(?P<slug>\d+)/$', views.agregar_detalle, name = 'agregar_detalle'),
	re_path('reporte_programa_pdf/(?P<programa_id>\d+)/$',
		view = views.ReporteProgramaPDF.as_view(),
		name= 'reporte_programa_pdf'
		),
	path('productosAsJson/', views.consultarProductosAsJson, name='productosAsJson'),
	path('categoriasAsJson/', views.consultarCategoriasAsJson, name='categoriasAsJson'),


    re_path('evento/inactivar/(?P<evento_id>\d+)/$', inactivar_evento, name = 'inactivar_evento'),
    path('lista-programas/', views.lista_programas, name = 'lista_programas'),

]