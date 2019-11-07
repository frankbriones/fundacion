"""Users models."""

# Django
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group




class Tipo_persona (models.Model):
#    TIPO_CAPACITADOR = 0
#    TIPO_VOLUNTARIO = 1
#    TIPO_CHOICES = (
#            (TIPO_CAPACITADOR, 'Capacitador'),
#            (TIPO_VOLUNTARIO, 'Voluntario'),
#        )
#
#    tipo  = models.SmallIntegerField(choices = TIPO_CHOICES, default = TIPO_VOLUNTARIO)
#   persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=100, null=True)



    def __str__(self):
        """Return username."""
        return '{}'.format(self.tipo)
    class Meta:
        
        verbose_name = "Tipo de Personal"
        verbose_name_plural = "Tipos de Persona"





#https://en.proft.me/2017/09/29/how-validate-file-size-imagefieldfilefiled-django/

class Persona (models.Model):


#    def validate_image (imagen):
#        file_size = image.file.size
#        limit_kb = 150
#        if file_size > limit_kb * 1024:
#            raise ValidationError ("El tamaño máximo del archivo es% s KB"% límite)




    SEXO_MASCULINO = 0
    SEXO_FEMENINO = 1
    
    SEXO_CHOICES = (
            (SEXO_MASCULINO, 'Masculino'),
            (SEXO_FEMENINO, 'Femenino'),
            
        )
    ESTADO_ACTIVO = 0
    ESTADO_INACTIVO = 1
    ESTADO_CHOICES = (
            (ESTADO_ACTIVO, 'Activo'),
            (ESTADO_INACTIVO, 'Inactivo'),
            
        )
    #IDIOMA_ESPANISH = 0
    #IDIOMA_ENGLISH = 1
    #IDIOMA_TWO = 2
    #IDIOMA_CHOICES = (
    #        (IDIOMA_ESPANISH, 'Espanol'),
    #        (IDIOMA_ENGLISH, 'Ingles'),
    #        (IDIOMA_TWO, 'Bilingue'),
    #    )
    
    cedula = models.CharField(max_length = 10,null = True, unique =True)
    nombres = models.CharField(max_length = 200, null = True)
    apellido_paterno =  models.CharField(max_length = 100, null = True)
    apellido_materno =  models.CharField(max_length = 100, null = True)
    sexo = models.SmallIntegerField(choices = SEXO_CHOICES, null = True)
    fecha_nacimiento = models.DateField(null = True)
    convencional = models.CharField(blank=True, max_length = 10, null=True)
    celular = models.CharField(max_length = 10, null = True)
    correo = models.EmailField()
    direccion = models.CharField(max_length = 300)
#    ocupacion = models.CharField(max_length = 100)
    #carrera = models.CharField(max_length = 100)
    #institucion = models.CharField(max_length = 200)
    #idioma = models.SmallIntegerField(choices = IDIOMA_CHOICES, null = True)
    estado = models.SmallIntegerField(choices = ESTADO_CHOICES, default = ESTADO_ACTIVO, blank=True)
    tipo = models.ForeignKey(Tipo_persona, on_delete=models.CASCADE, null=True, default='1', related_name="tipoP")
    edad = models.IntegerField(null=True)


    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(

        upload_to='persona/pictures',
        #validators= [validate_image]
        null=True,
        blank=True
    )
    
    
    def __str__(self):
        """Return username."""
        return '{} {} '.format(self.nombres, self.apellido_paterno)
    class Meta:
        
        verbose_name = "Tipo de Personal"
        verbose_name_plural = "Voluntarios/Capacitadores"











class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
Cree y guarde un usuario con el correo electrónico y la contraseña proporcionados."""
        if not email:
            raise ValueError('El correo electrónico dado debe estar configurado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False )
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        
        
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener superuser=True.')

        return self._create_user(email, password, **extra_fields)




from django.contrib.auth.models import Permission

from django.contrib.contenttypes.models import ContentType
from .validators import validate_file_extension

class Profile(AbstractUser):
    """User model."""


    
    username = None
    email = models.EmailField(_('Correo Electronico'), unique=True)
    nombres = models.CharField(max_length=50, null=True)

    apellidos = models.CharField(max_length=50, null=True)
    celular_regex = RegexValidator(
        regex = r'\+\d{9,15}$',
        message = "numero telefonico solo debe ser en el formato : +593999999. o 15 digitos permitidos."
        )
    celular = models.CharField( validators=[celular_regex], max_length=15, null=True)

    # imagen_regex = FileExtensionValidator(
    #     allowed_extensions= ['.jpg', '.png',]
    #     )
    imagen = models.ImageField(
        upload_to='users/pictures',
        null=True, 
        validators=[validate_file_extension],
        blank=True
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_verified = models.BooleanField(
        'Verificado',
        default= False,
            help_text='cuando el usuario verfica el correo,se verifica su cuenta'

        )
    is_staff = models.BooleanField(
        'Personal',
        default= False,
            help_text='Personal de la fundacion'

        )
    
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

    objects = UserManager()
    class Meta:
        permissions = (
            ('ver_detalle_persona', 'Puede ver detalle Persona'),
            )
        verbose_name = "perfil"
        verbose_name_plural = "Perfiles"


    def __str__(self):
        return '{}'.format(self.nombres)




''' CREE una vista en mi base de datos y luedo cree un modelo 
para renderizar esos datos de mi vista en el class meta: le digo que tabla de mi base se relacione con mi modelo..
y el enlace de ayuda...

https://resources.rescale.com/using-database-views-in-django-orm/
'''


class NID(models.Model):
    """docstring for tabla-genero"""
    id = models.IntegerField( primary_key=True)
    nombres = models.CharField(max_length=200)
    apellido_paterno = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10)
    correo = models.CharField(max_length= 254)
    fecha_nacimiento = models.CharField(max_length=15)
    edad = models.IntegerField(null=True)
    # tipo = models.CharField(max_length=10)
    estado = models.SmallIntegerField(null=True)

    def __str__(self):
        return '{}'.format(self.cedula)

    def save(self):
        super(NID, self).save()
    
    class Meta:
        managed = False
        db_table = 'nid'       
    