from django.shortcuts import render, reverse
from django.urls.base import reverse_lazy
import datetime
from django.http.response import HttpResponseRedirect, HttpResponse
import time
from persona.forms import PersonaForm, VoluntarioForm
from django.contrib.auth.decorators import login_required
from comentario.forms import ComentarioForm
from comentario.models import Comentario

# Create your views here.
def home(request):
	template='website/inicio.html'
	comentario = ComentarioForm()
	coment = Comentario.objects.filter(estado=0).order_by('-id')
	#.order_by('contenido')[:4]
	query = ''
	if 'query' in request.GET:
		query = request.GET['query']
		coment = coment
	paginator = Paginator(coment, 3)
	page = 1
	if 'page' in request.GET:
		page = int(request.GET['page'])
	pagina = paginator.page(page)


	data = {
		'date' : time.strftime("%d-%B-%Y"),
		'form': comentario,	
		'comentarios': pagina,
		'coment': coment,
	}
	return render(request, template, data)


def conocenos(request):
	template='website/conocenos.html'
	comentario = ComentarioForm()
	data = {
		'date' : time.strftime("%d-%B-%Y"),
		'form': comentario,	
	}
	return render(request, template, data)


def mision(request):
	template='website/misionv.html'
	comentario = ComentarioForm()
	data = {
		'date' : time.strftime("%d-%B-%Y"),
		'form': comentario,	
	}
	return render(request, template, data)


def programas(request):
	template='website/programasejec.html'
	comentario = ComentarioForm()
	data = {
		'date' : time.strftime("%d-%B-%Y"),
		'form': comentario,	
	}
	return render(request, template, data)


# def visitanos(request):
# 	template='website/visitanos.html'
# 	comentario = ComentarioForm()
# 	data = {
# 		'date' : time.strftime("%d-%B-%Y"),
# 		'form': comentario,	
# 	}
# 	return render(request, template, data)



from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
def nuevoVoluntario(request):
	template = 'website/voluntario/nuevo_voluntario.html'
	persona = None
	form = VoluntarioForm()
	if request.method == 'POST':
		form = VoluntarioForm(request.POST, request.FILES, instance = persona)
		#(form.data)
		if form.is_valid():
			persona = form.save()
			messages.success(request, 'TU INGRESO FUE CORRECTO!')
			return HttpResponseRedirect(reverse('website:inicio'))
	return render(request, template, {'form':form})



from django.contrib.auth import authenticate, login
from persona.forms import UserCreationForm, SignupForm



from talleres.models import Taller
from talleres.forms import EstudianteForm
from programa.models import Programa

#from talleres.forms import EstudForm
def nuevoEstudiante(request):
	template = 'website/estudiante/nuevo_estudiante.html'
	estudiante = None
	 
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			# messages.success(request, 'TAMBIEN FORMAS PARTE DE LOS ESTUDIANTES DE LA FUNDACION. BIENVENIDO')
			return HttpResponseRedirect(reverse('persona:login'))
	return render(request, template, {'form':form})



from django.shortcuts import render, redirect
from django.core.paginator import Paginator


from datetime import timedelta
import time
from datetime import datetime





def TalleresList(request):
	msg3 = None
	if 'msg3' in request.session:
		msg3 = request.session['msg3']
		del request.session['msg3']
	
	template = 'website/talleres_list.html'
	usuario = request.user

	try:
		msg = None
		if 'msg' in request.session:
			msg = request.session['msg']
			del request.session['msg']
		msgE = None
		if 'msgE' in request.session:
			msgE = request.session['msgE']
			del request.session['msgE']
		usuario = request.user
		
		talleres = Taller.objects.filter(estado=0).exclude(Estado_Estudiante_taller__estudiante__usuario = request.user.id).order_by('descripcion')
		talleres = talleres.filter(fecha_inicio__range= (datetime.now().date(),  datetime.now().date() + timedelta (days = 60)))
		t = Taller.objects.all()
		
			
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
		'talleres' : pagina,
		't': t,
		'msg' : msg,
		'msgE' : msgE,
		
		}
		#print(msg)
		return render(request, template, data)
	except Estudiante.DoesNotExist:
		#messages.success(request, 'No eres un estudiante {}'.format(usuario.nombres))
		template = 'website/inicio.html'
		request.session['msg3'] = "No eres un estudiante {}".format(usuario.nombres)
		data = {
		'msg3': msg3,
		}
		return render(request, template, data)




from persona.models import Profile
from talleres.models import Estado_Estudiante_taller, Estudiante
from django.db.models import Count


def estudiante_t(request, taller_id):
	usuario = request.user
	

	taller = Taller.objects.get(id=taller_id)
	estudiante = Estudiante.objects.all()
	e = Estado_Estudiante_taller.objects.filter(taller__id__exact=taller.id)
	print(taller.limite)
	if e.count() == taller.limite:
		request.session['msgE'] = "Cupo Limitado, No te Puedes Inscribir."
	else:
		try:
			estad = Estado_Estudiante_taller(taller=taller, estudiante=request.user.usuar, estado=0)
			estad.save()
			for x in estudiante:
				estado = Estado_Estudiante_taller.objects.filter(estudiante__id__exact=x.id).annotate(Count('taller_id'))
				x.contador_taller = estado.count()
				x.save() 
			
			request.session['msg'] = "Registrado en el Taller {}".format(taller.descripcion)
		except Estudiante.DoesNotExist:
			request.session['msg'] = "No eres estudiante "
			return HttpResponseRedirect(reverse('website:talleres'))
		
	return HttpResponseRedirect(reverse('website:talleres'))




from comentario.forms import ComentarioForm
from comentario.models import Comentario

# Create your views here.
def crear_comentario(request):
	template = "website/inicio.html"
	form = ComentarioForm(request.POST)
	
	if form.is_valid():
		comentario = form.save(commit=False)
		comentario.autor = request.user
		comentario.save()
		return HttpResponseRedirect(reverse('website:inicio'))
	data = {
	'form':form,
	}
	return render(request, template, data)