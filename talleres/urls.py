from django.urls import path, re_path
from talleres import views

urlpatterns = [
	path('', views.talleres, name='taller'),
	#api rest
	path('list/create/', views.create_taller, name='tallers'),
	path('list/', views.list_talleres, name='tallers'),


	path('realizados/', views.realizados, name='realizados'),
	path('lista-estudiantes/', views.estudiantes, name='estudiantes'),
	path('registro-taller/', views.taller_nuevo, name='nuevo_taller'),

	path('chart-data/talleres', views.chart_datas, name='chart_data'),
	path('chart-data/talleres-realizados', views.chart_datas_realizados, name='chart_data_realizados'),

	
	re_path('registro-estudiante/', views.nuevo_estudiante, name='nuevo_estudiante'),
	re_path('registro-estudiante/(?P<estudiante_id>\d+)/', views.nuevo_estudiante, name='nuevo_estudiante'),
	re_path('talleres-de-estudiante/(?P<estudiante_id>\d+)/', views.detalle_estudiante, name='detalle_estudiante'),


	
	re_path('detalle-taller/(?P<taller_id>\d+)/$', views.edit, name = 'edit'),
	re_path('reporte_estudiantes_pdf/(?P<taller_id>\d+)/$', view = views.ReportePersonasPDF.as_view(), name= 'reporte_estudiantes_pdf'),
	re_path('estado/(?P<estudiante_id>\d+)/$', views.abandonoEstudiante, name='estado2_estudiante'),
	re_path('agregar-taller-estudiante/(?P<estudiante_id>\d+)/$', views.talleresEstudiantes, name='talleres'),
	re_path('agregar-taller/(?P<estudiante_id>\d+)/(?P<taller_id>\d+)/$', views.estudiante_taller, name='estudiante_taller'),

	re_path('inactivar/(?P<taller_id>\d+)/$', views.inactivar_taller, name = 'inactivar_taller'),



	re_path('activar/(?P<taller_id>\d+)/$', views.activar_taller, name = 'activar_taller'),

	re_path('estado-estudiante/aprobado/(?P<estudiante_id>\d+)/$', views.aproboEstudiante, name='estado1_estudiante'),

	re_path('certificado-estudiante/(?P<profile_id>\d+)/(?P<taller_id>\d+)/$',
		view = views.pdfCertificado.as_view(),
		name='certificado'
		),

	re_path('verificar-pago/(?P<estudiante_id>\d+)/$', views.verificar_pago, name = 'verificar_pago'),
	

	#re_path('/Estudiante/(?P<estudiante_id>\d+)/(?P<taller_id>\d+)/$', views.estudiante_taller, name = 'estudiante_taller'),


]