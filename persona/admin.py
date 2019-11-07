"""User admin classes."""

# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Models
from django.contrib.auth.models import User
from persona.models import Profile, Persona, Tipo_persona, NID

#admin.site.register(NID)


#admin.site.register(Tipo_persona)



@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellido_paterno', 'correo', 'tipo', 'imagen', 'created')
    list_filter = ['estado', 'tipo', 'sexo']
    search_fields = ['cedula']

    fieldsets = (
        ('Datos Primarios', {
            'fields': (('cedula', 'nombres'),('apellido_paterno', 'apellido_materno')),
                    
        }),
        ('Extra info', {
            'fields': (('sexo', 'fecha_nacimiento', 'imagen'),('convencional', 'celular', 'correo'))
        }),
                 
        ('Extra info2', {
            'fields': (('direccion'),('estado'),('tipo'),('edad'))
        }),
      
        ('Metadata', {
            'fields': (('created', 'modified'),),
        })
    )

    readonly_fields = ('created', 'modified',)

    


#===============================================================================

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User


@admin.register(Profile)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model ."""

    fieldsets = (
        ('Claves de acceso', {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (('nombres', 'apellidos'), ('celular', 'imagen'))}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'nombres', 'apellidos', 'is_staff', 'is_active', 'is_verified')
    search_fields = ('email', 'nombres', 'apellidos')
    ordering = ('email',)
    verbose_name_plural = 'Perfiles'
#===============================================================================
#   
#   class ProfileInline(admin.StackedInline):
#       """Profile in-line admin for users."""
#  
# #     model = Profile
# #     can_delete = False
# #     verbose_name_plural = 'profiles'
# # 
# # 
# # class UserAdmin(BaseUserAdmin):
# #     """Add profile admin to base user admin."""
# # 
# #     inlines = (ProfileInline,)
# #     list_display = (
# #         'username',
# #         'email',
# #         'first_name',
# #         'last_name',
# #         'is_active',
# #         'is_staff'
# #     )
# # 
#===============================================================================
# 
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
#===============================================================================
