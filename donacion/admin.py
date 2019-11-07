from django.contrib import admin

# Register your models here.
from donacion.models import Donacion, Producto, Tipo, Categoria

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

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descripcion', 'fecha_expiracion', 'estado', 'donacion', 'cantidad', 'stock', 'condicion')
    search_fields = ['tipo__nombre']
    list_filter = ['estado', 'condicion']
    fieldsets = (
		('Datos Primarios', {
			'fields': (('descripcion', 'tipo'),('donacion', 'estado'), ('condicion',))
			}),
        ('Extra info', {
        	'fields': (('fecha_expiracion', 'cantidad'), ('stock', 'categoria'),)
        	}),
        ('Metadata', {
        	'fields': (('created', 'modified'),),
        	})
        )
    readonly_fields = ('created', 'modified')




class ProductoInline(admin.TabularInline):
    model = Producto
    readonly_fields = ('cantidad',)

    extra = 0
 
class DonacionAdmin(admin.ModelAdmin):
    inlines = [ProductoInline]
    list_display = ('estado', 'persona', 'usuario')
    search_fields = ['persona__nombres']
    list_filter = ['estado']
    fieldsets = (
		('Datos Primarios', {
			'fields': (('persona', 'estado'),('usuario'))
			}),
		
        ('Metadata', {
            'fields': (('created', 'modified'),),
            })
        )
    readonly_fields = ('created', 'modified')







@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'tipo', 'created', 'modified')
    search_fields = ['categoria']
    list_filter = ['tipo__nombre']
    readonly_fields = ('created', 'modified')
    
    




admin.site.register(Donacion, DonacionAdmin)
admin.site.register(Producto, ProductoAdmin)

#admin.site.register(Categoria)

#admin.site.register(Tipo)


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

