from django.contrib import admin
from comentario.models import Comentario
# Register your models here.
#example
#admin.site.register(Comentario)



@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'contenido', 'created', 'modified', 'estado',)
    search_fields = ['autor_nombres']
    #list_filter = ['tipo__nombre']
    readonly_fields = ('created', 'modified')
    
