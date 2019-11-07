from django.urls import path, re_path
from comentario import views


urlpatterns = [
	path(
        'list/',
        views.comentario_list,
        name='comentario_list'
        ),
	re_path(
        'eliminar/comentario/(?P<comentario_id>\d+)/',
        views.comentario_delete,
        name='comentario_delete'
        ),
	


]