from django.contrib import admin

# Register your models here.
from programa.models import Evento, Detalle, Programa


#===============================================================================
# 
# @admin.register(Tipo)
# class TipoAdmin(admin.ModelAdmin):
#     """Profile admin."""
# 
#     list_display = ('pk', 'nombre')
#     fieldsets = (
#         ('Tipo', {
#             'fields': (('nombre', 'ropa'    ),),
#             
#         }),
# 
#     )
#===============================================================================

class DetalleAdmin(admin.ModelAdmin):
	list_display = ('producto', 'tipo', 'cant', 'created', 'modified')
	search_fields = ['tipo__nombre']
	list_filter = ['programa__evento__nombre']

	fieldsets = (
		('Datos Primarios', {
			'fields': (('tipo', 'programa'),('producto', 'cant'))
			}),
        ('Metadata', {
        	'fields': (('created', 'modified'),),
        	})
        )
	readonly_fields = ('created', 'modified')


class DetalleInline(admin.TabularInline):
    model = Detalle
    extra = 1
 
class ProgramaAdmin(admin.ModelAdmin):
    inlines = [DetalleInline]
    list_display = ('evento', 'nombre', 'fecha_programa', 'fecha_culminacion', 'estado')
    list_filter = ['estado', 'evento__nombre']
    search_fields = ['nombre']
    fieldsets = (
		('Datos Primarios', {
			'fields': (('evento', 'nombre'),('fecha_programa', 'fecha_culminacion'))
			}),
		('Datos Extras', {
			'fields': (('direccion', 'persona'),('estado'))
			}),
        ('Metadata', {
        	'fields': (('created', 'modified'),),
        	})
        )
    readonly_fields = ('created', 'modified')



class EventoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'persona', 'estado', )
	list_filter = ['nombre']

	fieldsets = (
		('Datos Primarios', {
			'fields': (('nombre', 'estado'),('persona',),('imagen',))
			}),
        ('Metadata', {
        	'fields': (('created', 'modified'),),
        	})
        )
	readonly_fields = ('created', 'modified')


admin.site.register(Evento, EventoAdmin)

admin.site.register(Programa, ProgramaAdmin)
#admin.site.register(Detalle)

admin.site.register(Detalle, DetalleAdmin)
#===============================================================================
# class ProgramaAdmin(admin.ModelAdmin):
#     list_display = ('evento', 'descripcion')
#     fieldsets = (
#         ('Producto', {
#             'fields': (('evento', 'descripcion'),)
#         }),
#         ('Detalles', {
#             'fields': (
#                 ( 'fecha_culminacion', 'direccion'),
#                 ('tematica', 'cateogria')
#             )
#         })
#                  
#     )
#===============================================================================

