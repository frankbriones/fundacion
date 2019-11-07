# Django

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_viewsexit
from django.views.generic import UpdateView, FormView, DetailView
from persona.models import Profile
from django.urls.base import reverse, reverse_lazy
from django.shortcuts import render
from persona.models import Persona, Tipo_persona
from persona.forms import PersonaForm , SignupForm , ProfileForm
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse

from django.utils.translation import ugettext as _, ugettext_noop as _noop
from django.contrib.messages.context_processors import messages

from django.contrib.auth import authenticate, login
from persona.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from restapi.serializers import UserLoginSerializer



def signup2(request):
    template = "persona/signup2.html"
    form = UserCreationForm(request.POST or None)
    if form.is_valid():

        donacion = form.save(commit=False)
        donacion.save()
        request.session['msgu'] = "Ingreso de un Nuevo Usuario."
        slug = donacion.pk
        print(slug)
        # password = form.cleaned_data.get('password1')
        # username = form.cleaned_data.get('username')
        # user = authenticate(username=username, password=password)
        # login(request, user)
        return HttpResponseRedirect(reverse('persona:editar_user', kwargs={'profile_id': slug,}))
    return render(request, template, {'form': form})






def videos(request):
    template = 'website/new_html_video.html'
    return render(request,template)




def delete(request, profile_id):     
    user = Profile.objects.get(id=profile_id)
    request.session['msgeli'] = _("Usuario Elimiando ")
    user.is_active =  False
    user.save()
    #user.delete()
    
    return HttpResponseRedirect(reverse('persona:usuarios_list'))



from django.shortcuts import render, redirect
from django.core.paginator import Paginator

def usuarios_list (request):
    msgu = None
    
    if 'msgu' in request.session:
        msgu = request.session['msgu']
        del request.session['msgu']
    msgeli = None
    
    if 'msgeli' in request.session:
        msgeli = request.session['msgeli']
        del request.session['msgeli']


    template = 'persona/users.html' 
    usuarios  = Profile.objects.filter(is_active=True)

    query = ''

    if 'query' in request.GET:
        query = request.GET['query']
        usuarios = usuarios.filter(apellidos__istartswith = query)
        
    if 'query' in request.GET:
        query = request.GET['query']
        usuarios = usuarios
    paginator = Paginator(usuarios, 3)
    page = 1
    if 'page' in request.GET:
        page = int(request.GET['page'])
    pagina = paginator.page(page)




    data = {
    'usuarios': pagina,
    'msgu': msgu,
    'msgeli': msgeli,
    'usuaris':  usuarios,
    }
    return render(request,template, data)




def activar (request, persona_id):

    persona = Persona.objects.get(id=persona_id)
    persona.estado = 0
    persona.save()
    request.session['msg'] = "Vuelve a estar disponible la persona para dirigir un taller.."
    return HttpResponseRedirect(reverse('persona:list_capacitador_inactivos' ))


def inactivar (request, persona_id):
   
    persona = Persona.objects.get(id=persona_id)
    persona.estado = 1
    persona.save()
    request.session['msg'] = "Esta persona ya no podra dirigir algun taller, en las proximas fechas."
    return HttpResponseRedirect(reverse('persona:list_capacitador'))


@login_required
def list_capacitador(request):
    msg = None
    if 'msg' in request.session:
        msg = request.session['msg']
        del request.session['msg']
   

    template = 'persona/capacitador_list.html'
    personas = Persona.objects.filter(tipo__tipo__startswith = 'Capacitador')
    activos = personas.filter(estado = 0)
    #print(personas)
    data ={
    'personas': activos,
    'msg': msg,
    }
    return render(request, template, data)


@login_required
def talleres_list(request, persona_id):
    

    template = 'persona/talleres_list.html'
    talleres = Taller.objects.filter(persona__id__exact=persona_id)
    print(talleres)

    
    #print(personas)
    data ={
    'talleres': talleres
    }
    return render(request, template, data)




@login_required
def list_capacitador_inactivos(request):
    msg = None
    if 'msg' in request.session:
        msg = request.session['msg']
        del request.session['msg']

    template = 'persona/capacitadores_inactivos.html'
    personas = Persona.objects.filter(tipo__tipo__startswith = 'Capacitador')
    inactivos = personas.filter(estado = 1)
    #print(personas)
    data ={
    'personas': inactivos,
    'msg': msg,
    }
    return render(request, template, data)




@login_required
def editar_perfil_user(request, profile_id):
    profile = Profile.objects.get(id=profile_id)

    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('persona:usuarios_list'))
    return render(request, 'persona/editar_usuario.html', {'form': form, 'profile': profile,})





@login_required
def editar_perfil(request):
    profile = request.user
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('persona:update'))
    return render(request, 'persona/editar_perfil.html', {'form': form, 'profile': profile,})



@login_required
def detalle(request, persona_id):
    template = 'persona/detalle_voluntario.html'
    persona = Persona.objects.get(id=persona_id)
    data =  {
    
    'persona': persona,
    }
    return render(request, template, data)

from persona.forms import VoluntarioForm

@login_required
def edicion(request, persona_id):
    persona = Persona.objects.get(id=persona_id)
    form = PersonaForm(instance=persona)
    print(persona.created)
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES, instance=persona)
        if form.is_valid():
            form.save()
            request.session['msg1'] = "Actualizacion de Voluntario Finalizado"
            return HttpResponseRedirect(reverse('persona:personas'))
    
    return render(request, 'persona/editar_voluntario.html', {'form': form, 'persona': persona,})




class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'persona/login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'persona/logged_out.html'
    

from django.shortcuts import get_object_or_404

#class UserDetailView(LoginRequiredMixin, DetailView):
#    def get(self, request, *args, **kwargs):
#        profile = get_object_or_404(Profile, pk=kwargs['pk'])
#        context = {'profile': profile}
#        return render(request, 'persona/detalle_perfil.html', context)


from django.core.paginator import Paginator


from talleres.models import Estudiante, Taller, Estado_Estudiante_taller

from django.contrib.auth.models import Permission

from django.contrib.contenttypes.models import ContentType

@login_required
def UpdateProfileView(request):
    """Update profile view."""

    template = 'persona/detalle_perfil.html'
    usuario = request.user
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    print(num_visits)
    
    try:

        estudiante = Estudiante.objects.get(usuario__id__exact=usuario.id)
        talleres = Taller.objects.filter(Estado_Estudiante_taller__estudiante =estudiante.id).order_by('descripcion')

        talleres2 = Taller.objects.filter(estado=0).exclude(Estado_Estudiante_taller__estudiante=estudiante.id)
        
        
        estado = Estado_Estudiante_taller.objects.filter(estudiante__id__exact=estudiante.id)
       
        query = ''
        if 'query' in request.GET:
            query = request.GET['query']
            talleres = talleres
        paginator = Paginator(talleres, 2)
        page = 1
        if 'page' in request.GET:
            page = int(request.GET['page'])
        pagina = paginator.page(page)

        data = {
        'talleres': pagina,
        'estudiante': estudiante,
        'estado': estado,
        'profile': usuario,
        'talleres2': talleres2,
        'num_visits':num_visits

        }


        return render(request, template, data)
    except Estudiante.DoesNotExist:
        template = 'persona/detalle_perfil.html'

        data = {
        
        'profile': usuario,
        'num_visits':num_visits

        }
        return render(request, template, data)

   

    
from django.db.models import Count, Q
from persona.models import NID


from datetime import timedelta
import time
from datetime import datetime, date



@login_required
def personas(request):
    msg1 = None
    if 'msg1' in request.session:
        msg1 = request.session['msg1']
        del request.session['msg1']

    msgV = None
    if 'msgV' in request.session:
        msgV = request.session['msgV']
        del request.session['msgV']

    personas = NID.objects.filter(estado=0)

    #calculo de edad en la vista de personas_list
    hoy = date.today()
    for x in personas:
        tipo = Tipo_persona
        e = (hoy) - (x.fecha_nacimiento) 
        e = e.days
        edad_numerica = e / 365.2425 #anio gregoriano
        edad_n = int(edad_numerica)
        x.edad = edad_n
        
        x.save()
        
    
    template = 'persona/persona_list.html'

    hombres = Persona.objects.filter(sexo=0).annotate(Count('id'))


    mujeres = Persona.objects.filter(sexo=1).annotate(Count('id'))
    total = Persona.objects.annotate(Count('id'))
  
    data = {
        #'cant': cant,
        'personas': personas,
        'msg1': msg1,
        'hombres': hombres,
        'mujeres': mujeres,
        'total': total,
        'edad': edad_n,
        'msgV': msgV

    }    
    return render(request, template, data)

@login_required
def nuevaPersona(request):
    template = 'persona/nuevo_voluntario.html'
    persona = None
    form = PersonaForm()
    
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES, instance = persona)
        #(form.data)
        if form.is_valid():
            persona = form.save()
            request.session['msgV'] = "Ingreso de Voluntario Finalizado"
            return HttpResponseRedirect(reverse('persona:personas'))

    return render(request, template, {'form':form})
#===============================================================================


# class SignupView(FormView):
#     """Users sign up view."""

#     template_name = 'persona/signup.html'
#     form_class = SignupForm
#     success_url = reverse_lazy('persona:usuarios_list')

#     def form_valid(self, form):
#         """Save form data."""
#         form.save()
#         return super().form_valid(form)



from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Tu password fue actualizada correctamente!')
            return redirect('persona:change_password')
        else:
            messages.error(request, 'Encontramos errores en tu peticion')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'persona/change_password.html', {
        'form': form
    })




#https://simpleisbetterthancomplex.com/tutorial/2018/04/03/how-to-integrate-highcharts-js-with-django.html
import json
def chart_data(request):
    dataset = Persona.objects \
        .values('sexo')\
        .annotate(hombres=Count('sexo', filter=Q(sexo=0)))\
        .exclude(sexo=1)\
        .exclude(sexo=2)  
    dataset2 = Persona.objects \
        .values('sexo')\
        .annotate(mujeres=Count('sexo', filter=Q(sexo=1)))\
        .exclude(sexo=0)\
        .exclude(sexo=2)
    # dataset3 = Persona.objects \
    #     .values('sexo')\
    #     .annotate(indef=Count('sexo', filter=Q(sexo=2)))\
    #     .exclude(sexo=1)\
    #     .exclude(sexo=0)


    hombres = Persona.objects.filter(sexo=0).annotate(Count('id'))


    mujeres = Persona.objects.filter(sexo=1).annotate(Count('id'))
    total = Persona.objects.annotate(Count('id'))

    categories=list()
    hombre_s = list()
    mujer_s=list()
    #indefinido_s=list()
    for entradah in dataset:
        hombre_s.append(entradah['hombres'])
        
    for entradam in dataset2:
        mujer_s.append(entradam['mujeres'])
        print(mujer_s)
    # for entradai in dataset3:
    #     indefinido_s.append(entradai['indef'])
    #     print(indefinido_s)
    data = {
    'hombre_s': json.dumps(hombre_s),
    'mujer_s': json.dumps(mujer_s),
    #'indefinido_s': json.dumps(indefinido_s),
    'personas': Persona.objects.filter(estado = Persona.ESTADO_ACTIVO),
    
    'hombres': hombres,
    'mujeres': mujeres,
    'total': total
    }



    return render(request, 'persona/chart.html', data)


#    sexo_display_name = dict()
#    for sexo_tuple in Persona.SEXO_CHOICES:
#        sexo_display_name[sexo_tuple[0]] = sexo_tuple[1]
#
#    chart = {
#        'chart': {'type': 'area'},
#        "xAxis": '',
#        'title': {'text': 'TOTAL DE VOLUNTARIOS DE ACUERDO AL GENERO'
#
#            },
#        'series': [{
#            'name': 'Total',
#            'data': list(map(lambda row: {'name': sexo_display_name[row['sexo']], 'y': row['total']}, dataset)),
            #'color': 'orange'
#        }

#        ],
        
#    }
    #print(dataset)
#    return JsonResponse(chart)
from persona.forms import ContactoForm

from django.core.mail.message import EmailMessage

@login_required
def contacMail(request):
    templates = 'persona/correo.html'
    formulario = ContactoForm()
    usuarios = Profile.objects.filter(is_active = True).order_by('email')
    usuarios = usuarios.filter(is_staff=True)
    # users = Profile.objects.filter(is_staff=True).filter(is_active=True)
    # print(users)

    
    
    if request.method == 'POST':
        formulario = ContactoForm(request.POST, request.FILES)
        if formulario.is_valid():
            asunto = "Fundacion Tacita Caliente le notifica. "
            mensaje = formulario.cleaned_data['mensaje']
            correo = formulario.cleaned_data['correo']
            mail = EmailMessage(asunto, mensaje, to=[correo])
            mail.send()
            return HttpResponseRedirect(reverse('persona:correo'))
    query = ''

    if 'query' in request.GET:
        query = request.GET['query']
        usuarios = usuarios.filter(apellidos__istartswith = query)
    
    if 'query' in request.GET:
        query = request.GET['query']
        usuarios = usuarios
    paginator = Paginator(usuarios, 2)
    page = 1
    if 'page' in request.GET:
        page = int(request.GET['page'])
    pagina = paginator.page(page)
    datos = {
        'formulario': formulario,
        'usuarios': pagina,
        'users': usuarios
            }
    return render(request, templates, datos)