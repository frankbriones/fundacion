from django.contrib import admin

# Register your models here.
from talleres.models import Taller, Estudiante, Categoria_taller, Estado_Estudiante_taller, Horario


#manytomany
#class EstudianteInline(admin.TabularInline):
#    model = Estudiante.taller.through
#    extra = 0
class TallerInline(admin.TabularInline):
	model = Taller
	extra=0
class HorarioAdmin(admin.ModelAdmin):
	inlines=[TallerInline]


class EstadoAdmin(admin.ModelAdmin):
	readonly_fields = ('estado','estudiante','inscrito')
	list_display = ( 'estado', 'taller', 'estudiante', 'created')
	search_fields = ['estudiante__usuario__nombres']
	list_filter =['estudiante__usuario__nombres', 'estado']



class EstadoInline(admin.TabularInline):
	model = Estado_Estudiante_taller
	extra=0

class EstudianteAdmin(admin.ModelAdmin):
	inlines = [EstadoInline]
	list_display = ('id', 'usuario', 'contador_taller')
	fieldsets = (
		('Datos de usuario', {
			'fields': (('usuario'),('contador_taller'))
			}),
		)
	search_fields = ['usuario']
	list_filter =['usuario__nombres']
	readonly_fields=['contador_taller']



def activar_taller(modeladmin, request, queryset):
    queryset.update(estado=Taller.TIPO_ACTIVO)
activar_taller.short_description = "Activar talleres masivamente"


 
class TallerAdmin(admin.ModelAdmin):
	inlines = [EstadoInline]
	search_fields = ['descripcion']
	list_filter =['categoria', 'estado']
	ordering = ('fecha_culmina',)

	actions = [activar_taller]

	list_display = ('descripcion',  'categoria', 'fecha_inicio',  'fecha_culmina', 'horario', 'active', 'precio', 'estado')

	fieldsets = (
		('Datos Primarios', {
			'fields': (('descripcion', 'detalle'),('active', 'estado' ), ('precio'),)
			}),
        ('Extra info', {
        	'fields': (('fecha_inicio', 'fecha_culmina'),('persona', 'categoria'),('limite', 'horario'))
        	}),
        ('Metadata', {
        	'fields': (('created', 'modified'),),
        	})
        )
	readonly_fields = ('created', 'modified')





admin.site.register(Taller, TallerAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Estudiante, EstudianteAdmin )

#admin.site.register(Estado_Estudiante_taller )
admin.site.register(Estado_Estudiante_taller, EstadoAdmin )