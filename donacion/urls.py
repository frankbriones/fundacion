from django.urls import path, re_path
from donacion import views
from donacion.views import inactivar, inactivar2, inactivar3, nuevaDonacion
urlpatterns = [
	path('lista-donaciones/', views.donacion, name = 'donaciones'),
	
	path(
		'registro-donacion/',
		views.nuevaDonacion,
		name = 'donacion'
	),


	re_path('editar-donacion/(?P<donacion_id>\d+)/$', views.edit, name = 'edit'),
	re_path('registro-producto/donacion/(?P<slug>\d+)/$', views.producto, name = 'producto'),
	
	re_path('reporte_donacion_pdf/(?P<donacion_id>\d+)/$',
		view = views.ReporteDonacionPDF.as_view(),
		name= 'reporte_donacion_pdf'
		),
	re_path(r'^imprimir/(?P<donacion_id>\d+)/$',
		view = views.show_donacion,
		name= 'show_donacion'
		),
    path('productos-por-expirar/', views.productos_expiran, name = 'expira'),

    path('stock-productos/', views.stock_total, name = 'stock_total'),

    re_path('productos/inactivar/(?P<producto_id>\d+)/$', inactivar, name = 'inactivar'),
    re_path('productos/inactivar2/(?P<producto_id>\d+)/$', inactivar2, name = 'inactivar2'),
    re_path('productos/inactivar3/(?P<producto_id>\d+)/$', inactivar3, name = 'inactivar3'),


    path('reportes/', views.reportes, name = 'reportes'),

    path('reportes/talleres/', views.reporte_talleres, name = 'reporte_talleres'),
    path('reportes/voluntarios/', views.reporte_voluntarios, name = 'reporte_voluntarios'),
    path('reportes/programas/', views.reporte_programas, name = 'reporte_programas'),

    path('reportes/donaciones/', views.reporte_donaciones, name = 'reporte_donaciones'),

	path('chart-data/', views.chart_data2, name='chart_data2'),

	
	path('categoriasAsJson/', views.consultarCategoriasAsJson, name='categoriasAsJson'),

	re_path('productos-en-bodega-expiraron/$',
		view = views.descompuesto,
		name= 'descompuesto'
		),

]