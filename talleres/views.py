from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from talleres.forms import TallerForm, EstudianteForm
from talleres.models import Taller, Estudiante

from persona.models import Persona

from django.urls.base import reverse, reverse_lazy

from django.contrib.auth.decorators import login_required



from datetime import timedelta
import time
from datetime import datetime



#@login_required
#def talleresEstudiantes(request, estudiante_id):
#	template =  'taller/agregar_taller_list.html'
#	estudiante = Estudiante.objects.get(id=estudiante_id)
#	talleres = estudiante.taller.all()
#	tallers=None
#	for x in talleres:
#		tallers = Taller.objects.filter(estado=0).exclude(estudiante=estudiante_id)
#		tallers = tallers.filter(fecha_inicio__range= (datetime.now().date(),  datetime.now().date() + timedelta (days = 365)))
#		print(tallers)
#	data = {
#	'estudiante': estudiante,
#	'talleres': tallers
#	}
#	return render(request, template, data)


#restframeworkk
from talleres.models import Horario
from talleres.serializers import TallerSerializer, CreateTallerSerializer
from rest_framework.decorators import  api_view
from rest_framework.response import  Response



# @api_view(['GET'])
# def list_talleres(request):
# 	queryset = Taller.objects.filter(estado=0)
# 	datos = []
# 	fecha_actual = datetime.now().date()
# 	for query in queryset:
# 		datos.append({
# 			'descripcion' : query.descripcion,
# 			'created': query.created,
# 			'detalle': query.detalle,
# 			'estado': query.estado,
# 			'fecha_inicio': query.fecha_inicio,

# 			'fecha_culmina': query.fecha_culmina,
# 			'precio': query.precio,
# 			'horario': query.horario.hora,
# 			'persona': query.persona.nombres,
# 			})
# 		return Response(datos)
# 	#print(datetime.now().date()) 


# @api_view(['POST'])
# def create_taller(request):
	
# 		descripcion = request.data['descripcion']
# 		detalle= request.data['detalle']
# 		fecha_inicio= request.data['fecha_inicio']
# 		fecha_culmina= request.data['fecha_culmina']
# 		precio = request.data['precio']
# 		horario = request.data['horario']
# 		persona = request.data['persona']
# 		estado = request.data.get('estado', 0)
# 		taller = Taller.objects.create(
# 			descripcion=descripcion,
# 			detalle=detalle,
# 			estado=estado,
# 			fecha_inicio=fecha_inicio,
# 			fecha_culmina=fecha_culmina,
# 			precio=precio,
# 			horario=Horario.objects.get(hora=horario),
# 			persona=Persona.objects.get(nombres=persona),
# 			)
# 		data = {
# 		'descripcion': 	taller.descripcion,
# 		'estado': taller.estado,
# 		'fecha_inicio': taller.fecha_inicio,
# 		'fecha_culmina': taller.fecha_culmina,
# 		'horario': taller.horario.hora,
# 		'persona': taller.persona.nombres

# 		}
# 		return Response(data)




""" 
Detalle del Estudiante
"""
from django.contrib.auth.decorators import permission_required


@permission_required('taller.add_taller')
@login_required
def detalle_estudiante(request, estudiante_id):
	template = 'taller/detalle_estudiante.html'
	estudiante = Estudiante.objects.get(id=estudiante_id)
	talleres = Taller.objects.filter(Estado_Estudiante_taller__estudiante =estudiante.id).order_by('descripcion')
	e = Estado_Estudiante_taller.objects.filter(estudiante__id__exact=estudiante.id).order_by('taller')
	print(e)
	fecha_actual = datetime.now().date()
	for t in e:
		if t.taller.fecha_inicio < fecha_actual and t.estado == 0:
			t.estado = 2
			t.save(update_fields=['estado'])

		
	
	data = {
	'estudiante' : estudiante,
	'talleres' : e
	}
	return render(request, template, data)


@api_view(['GET'])
def list_talleres(request):
	talleres = Taller.objects.filter(estado=0).order_by('fecha_inicio')
	#fecha_actual = datetime.now().date()
	serializer = TallerSerializer(talleres, many=True)
	return Response(serializer.data)


@api_view(['POST'])
def create_taller(request):
	"""crear tallerr"""
	serializer = CreateTallerSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	data = serializer.data
	taller = Taller.objects.create(**data)
	return Response(data)






"""no django rest"""
from datetime import date

@login_required
def estudiante_taller(request, taller_id, estudiante_id):
	fecha_actual = datetime.now().date()
	estudiante = Estudiante.objects.get(id=estudiante_id)
	taller = Taller.objects.get(id=taller_id)
	estad = Estado_Estudiante_taller(taller=taller, estudiante=estudiante, estado=0, inscrito=fecha_actual)
	estad.save()
	request.session['msg5'] = "Agregado al taller {}, el estudiante: {}".format(taller.descripcion, estudiante)
	
	return HttpResponseRedirect(reverse('tallers:talleres', kwargs={'estudiante_id': estudiante_id,} ))


@login_required
def talleresEstudiantes(request, estudiante_id):
	msg5 = None
	if 'msg5' in request.session:
		msg5 = request.session['msg5']
		del request.session['msg5']
	template =  'taller/agregar_taller_list.html'
	estudiante = Estudiante.objects.get(id=estudiante_id)
	talleres = Taller.objects.filter(estado=0).exclude(Estado_Estudiante_taller__estudiante=estudiante_id)
	talleres = talleres.filter(fecha_inicio__range= (datetime.now().date(),  datetime.now().date() + timedelta (days = 365)))
	print(msg5)
	data = {
	'estudiante': estudiante,
	'talleres': talleres,
	'msg5': msg5,
	}
	return render(request, template, data)




@login_required
def activar_taller (request, taller_id):
    taller = Taller.objects.get(id=taller_id)
    taller.estado = 0
    taller.save()
    return HttpResponseRedirect(reverse_lazy('tallers:taller'))




@login_required
def inactivar_taller (request, taller_id):
    taller = Taller.objects.get(id=taller_id)
    taller.estado = 1
    taller.save()
    return HttpResponseRedirect(reverse_lazy('tallers:taller'))



@login_required
def verificar_pago (request, estudiante_id):
	e = Estado_Estudiante_taller.objects.get(id=estudiante_id)
	taller = Taller.objects.get(id=e.taller.id)
	taller = taller.id
	e.pago = 0
	e.save()
	return HttpResponseRedirect(reverse('tallers:edit', kwargs={'taller_id': taller,} ))






#from django.urls.base import reverse_lazy

# Create your views here.
@login_required
def abandonoEstudiante(request, estudiante_id ):

	estado = Estado_Estudiante_taller.objects.get(id=estudiante_id)
	taller = Taller.objects.get(id=estado.taller.id)
	taller = taller.id
	estado.estado = 2
	estado.save()
	return HttpResponseRedirect(reverse('tallers:edit', kwargs={'taller_id': taller,} ))
		#kwargs={'taller_id': taller,} ))






#def abandonoEstudiante(request, estudiante_id ):
#	#estudiante = Estudiante.objects.get(id=estudiante_id)
#	#taller = Estudiante.objects.get(taller__id__exact=estudiante.id)
#	estado = Estado_Estudiante_taller.objects.filter(id=estudiante_id)
#
#	for x in estado:
#		print('estado:', x)
#		x.estado = 2
#		x.save()
#
#	return HttpResponseRedirect(reverse('tallers:taller'))
		#kwargs={'taller_id': taller,} ))


	

@login_required
def aproboEstudiante(request,  estudiante_id, *args, **kwargs):
	#estudiante = Estudiante.objects.get(id=estudiante_id)
	estado = Estado_Estudiante_taller.objects.get(id=estudiante_id)
	taller = Taller.objects.get(id=estado.taller.id)
	taller = taller.id
	print(taller)
	#for x in estado:
	#	print('estado:', x)
	#	x.estado = 1
	#	x.save()
	print(estado)
	estado.estado = 1
	estado.save()
	#estado=1
	#estado.save()

	return HttpResponseRedirect(reverse('tallers:edit', kwargs={'taller_id': taller,} ))
		#, kwargs={'taller_id': taller,} ))



from talleres.forms import EstudianteForm
from persona.forms import SignupForm
from django.db import transaction
from django.contrib.auth.decorators import permission_required
#@login_required

from django.contrib import messages

# @permission_required('persona.add_profile')
# @transaction.atomic
def nuevo_estudiante(request, estudiante_id = None):
	template ='taller/nuevo_estudiante.html'

	form = SignupForm()
	estudiante= None
	
	if request.method == 'POST':
		form = SignupForm(request.POST, request.FILES)
		(form.data)
		if form.is_valid():
			estudiante = form.save()
			request.session['msge'] = "Ingreso de Estudiante Realizado!"
			return HttpResponseRedirect(reverse('tallers:taller'))
	return render(request, template, {'form':form})


from talleres.models import  Estado_Estudiante_taller




@login_required

def estudiantes(request):
	template = 'taller/estudiantes_list.html'
	queryset = None

	queryset = Estudiante.objects.all()
	for query in queryset:
		estado = Estado_Estudiante_taller.objects.filter(estudiante__id__exact=query.id).annotate(Count('taller_id'))
		query.contador_taller = estado.count()
		query.save()

	date = time.strftime("%Y")
	data = {
		'estudiantes': queryset,
		'date': date,
		'estado': estado,

	}
	return render(request,template, data)











from django.core.paginator import Paginator

#@api_view(['GET'])

@login_required
def talleres(request):
	msgt = None
	if 'msgt' in request.session:
		msgt = request.session['msgt']
		del request.session['msgt']

	msge = None
	if 'msge' in request.session:
		msgt = request.session['msge']
		del request.session['msge']

	fecha_actual = datetime.now().date()
	


	template = 'taller/taller_list.html'
	# queryset = Taller.objects.filter(fecha_culmina__range= (datetime.now().date() - timedelta(days=1),  datetime.now().date() + timedelta (days = 365))).filter(estado=0)
	# queryset = Taller.objects.filter(estado=0)

	queryset2 = Taller.objects.all()
	
	queryset = Taller.objects.filter(fecha_culmina__range= (datetime.now().date() - timedelta(days=1),  datetime.now().date() + timedelta (days = 365)))
	
	'''Proceso para cada taller, realizar un cambio de estado si el taller ah culminado
				en su totalidad'''
	for query in queryset:
		if query.fecha_culmina <= fecha_actual:

			query.estado = 1
			query.save(update_fields=['estado'])
		estados = Estado_Estudiante_taller.objects.filter(taller__id__exact=query.id)
		for estado in estados:
			if estado.taller.fecha_inicio < fecha_actual:
				estado.estado = 2
				estado.save()
		
	#print(datetime.now().date())

	query = ''
	if 'query' in request.GET:
		query = request.GET['query']
		queryset = query
	paginator = Paginator(query, 2)
	page = 1
	if 'page' in request.GET:
		page = int(request.GET['page'])
	pagina = paginator.page(page)


	realizados = Taller.objects.filter(estado=1)

	date = time.strftime("%Y")
	data = {
		'talleres': pagina,
		'tallers' : queryset,
		'date': date,
		'msgt': msgt,
		'msge': msge,
		'realizados': realizados,
		'queryset2': queryset2
	}
	return render(request,template, data)


def realizados(request):
	template = 'taller/taller_realizados.html'
	queryset = Taller.objects.filter(estado=1)
	
	data = {
	'talleres': queryset
	}
	return render(request, template, data)



@login_required
def taller_nuevo(request):
	template = 'taller/nuevo_taller.html'	

	form = TallerForm()
	
	if request.method == 'POST':
		form = TallerForm(request.POST, request.FILES)
		if form.is_valid():
			
			taller = form.save()
			request.session['msgt'] = "Ingreso de Taller Realizado!"
			return HttpResponseRedirect(reverse('tallers:taller'))

	else:
		form = TallerForm()

	data = { 
			'form': form,
		}
	return render(request, template, data)





@login_required
def edit(request, taller_id):
    template = 'taller/detalle_taller.html'
    taller = Taller.objects.get(id=taller_id)
    fecha_actual = datetime.now().date()

    estudiantes = Estado_Estudiante_taller.objects.filter(taller__id__exact=taller_id)
    if taller.fecha_culmina <= fecha_actual and  taller.estado == 1:
    	for x in estudiantes:
    		if x.estado == 0:
    			x.estado = 2
    			x.save(update_fields=['estado'])
    	

    # fecha_actual = datetime.now().date()
    # if taller.fecha_inicio < fecha_actual and t.estado == 0:
    # 		e.estado = 2
    # 		t.save(update_fields=['estado'])



    if taller.precio == None or taller.precio == 0:

    	for estudiante in estudiantes:
    		
    		estudiante.pago = 0
    		estudiante.save()
    		
    #print(estudiantes)
    data = {
    	'taller':taller,
    	'estudiantes': estudiantes
    }
    return render(request, template, data)


from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

from django.http import FileResponse
from django.utils.translation import gettext 

class ReportePersonasPDF(View):
	#taller = Taller.objects.get(taller__id__exact='taller_id')

	def cabecera(self,pdf, *args, **kwargs):
		taller = self.kwargs.get('taller_id')
		self.taller =  taller
		#print(taller)
		archivo_imagen = settings.MEDIA_ROOT+'/imagenes/logos.jpg'
		
		pdf.drawImage(archivo_imagen, 30, 700, 200, 150,preserveAspectRatio=True)
		pdf.setFont("Helvetica", 20)
		pdf.drawString(250, 790, u"'Fundacion Tacita Calietne'")
		pdf.setFont("Helvetica", 14)
		pdf.drawString(300, 770, u"Lista de Asistencias ")
		pdf.setFont("Helvetica", 12)
		
		pdf.drawString(350, 50, u"Firma: _______________________")

	def tabla(self,pdf,y, taller_id):
		taller = Taller.objects.get(id= taller_id)
		self.taller = taller
		self.taller.fecha_inicio = taller.fecha_inicio
		date = time.strftime("%d/%B/%Y")
		print('taller: ', self.taller.fecha_inicio)
		pdf.drawString(300, 700, (" Fecha : " + date))
		pdf.setFont("Helvetica", 12)
		pdf.drawString(300, 680,(" Taller : " + str(self.taller) ))
		pdf.setFont("Helvetica", 14)
		estudiante = Estado_Estudiante_taller.objects.filter(taller__id__exact=taller_id)
		encabezados = ('NOMBRES', 'APELLIDOS', 'CORREO', 'Asist.')
		altX = 630
		detalles = [( estudiante.estudiante.usuario.nombres, estudiante.estudiante.usuario.apellidos, estudiante.estudiante.usuario.email)
		for estudiante in estudiante]
		for detalle in detalles:
				altX = altX - 18

		if estudiante :
				detalle_orden = Table([encabezados] + detalles, colWidths=[ 3.5 * cm, 3.5 * cm, 7* cm, 2 * cm])
				detalle_orden.setStyle(TableStyle(
	            [
	                #La primera fila(encabezados) va a estar centrada
	                ('ALIGN',(0,0),(3,0),'CENTER'),
	                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
	                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
	                #El tamaño de las letras de cada una de las celdas será de 10
	                ('FONTSIZE', (0, 0), (-1, -1), 10),
	            ]
	        ))
				detalle_orden.wrapOn(pdf, 800, 600)
				detalle_orden.drawOn(pdf, 60, altX)
				#print(taller)
	def get(self, request, *args, **kwargs):
		taller = self.kwargs.get('taller_id')
		#print(taller)
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'inline; filename=Lista_Estudiantes.pdf'
		buffer = BytesIO()
		pdf = canvas.Canvas(buffer)
		self.cabecera(pdf)
		y = self.tabla
		self.tabla(pdf, y, taller)
		pdf.showPage()

		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response


#crear la grafica los talleres por categoria en el template


from django.db.models import Count
def chart_datas(request):
    dataset = Taller.objects \
        .values('categoria') \
        .annotate(total= Count('categoria'))\
        

    categoria_display_name=dict()
    for categoria_tuple in Taller.CATEGORIA_CHOICES:
        categoria_display_name[categoria_tuple[0]] = categoria_tuple[1]

        

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'TALLERES DE ACUERDO A LA CATEGORIA'},
        'series': [{
            'name': 'total de talleres',
            'data': list(map(lambda row: {'name': categoria_display_name[row['categoria']], 'y': row['total']}, dataset))
        }]
        
    }
    #print(dataset)
    return JsonResponse(chart)



from django.db.models import Count
def chart_datas_realizados(request):
    dataset = Taller.objects \
        .values('categoria') \
        .annotate(total= Count('categoria'))\
        .filter(estado=1)
    print(dataset)

    categoria_display_name=dict()
    for categoria_tuple in Taller.CATEGORIA_CHOICES:
        categoria_display_name[categoria_tuple[0]] = categoria_tuple[1]

        

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'TALLERES EJECUTADOS'},
        'series': [{
            'name': 'total de talleres',
            'data': list(map(lambda row: {'name': categoria_display_name[row['categoria']], 'y': row['total']}, dataset))
        }]
        
    }
    #print(dataset)
    return JsonResponse(chart)


from persona.models import Profile

from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.lib.pagesizes import landscape, letter, A4
from reportlab.lib.units import inch

from reportlab.lib.colors import pink, green, brown, white, blue, grey, black, red
class pdfCertificado(View):

	def cabecera(self,pdf):
			

			
			archivo_imagen2 = settings.MEDIA_ROOT+'/imagenes/sello2.jpg'
			#Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
			pdf.drawImage(archivo_imagen2, 600, 0, 200, 900,preserveAspectRatio=True)
			pdf.setFont('Helvetica-Bold', 12)
			pdf.setFillColorRGB(0.,0.,0.5)
			pdf.drawCentredString(415, 535, "FUNDACION")

			pdf.setFont('Helvetica-Bold', 40)
			pdf.setFillColor(black)
			pdf.drawCentredString(415, 500, "Tacita Caliente")

			pdf.setFont('Helvetica', 15)
			pdf.setFillColorRGB(0.,0.,0.5)
			pdf.drawCentredString(415, 430, "Certifica a:")
			pdf.setFont("Helvetica", 15)
			pdf.drawCentredString(415, 380, "Por participar y aprobar el")
			pdf.setFont("Helvetica", 10)
			pdf.drawCentredString(610, 110, "Rebeca Medina.")
			pdf.setFont("Helvetica", 10)
			pdf.drawCentredString(220, 110, "Christian Alava.")


			pdf.setFont("Helvetica", 25)
			pdf.setFillColorRGB(0.,0.,0.5)
			pdf.drawCentredString(415, 300, "TALLER DE")

			
			pdf.setFont("Helvetica-Bold", 10)
			pdf.setFillColor(brown)
			pdf.drawCentredString(220, 97, "Director de Fundacion")
			pdf.setFillColor(brown)
			pdf.setFont("Helvetica-Bold", 10)
			pdf.drawCentredString(610, 97, "Directora de Fundacion")


			


			pdf.setFont("Helvetica", 8)
			pdf.setFillColor(blue)
			pdf.drawCentredString(415, 50, "CERTIFICADO DE APROBACION ONLINE.")

			pdf.setFont("Helvetica-Bold", 10)
			pdf.setFillColor(black)
			pdf.drawCentredString(415, 40, "https://fundaciontacita.com/")

			#pdf.setFillColorRGB(0. ,0.8,0.8)
			#pdf.circle(70,515,70,stroke=1,fill=1)
			#pdf.setStrokeColor(brown)
			#pdf.line(250,0,0, 150)
			#pdf.setStrokeColor(green)
			#pdf.line(80,0,150,600)
			pdf.setStrokeColor(black)
			pdf.line(120,120,300,120)
			pdf.setStrokeColor(black)
			pdf.line(510,120,710,120)

			
			
			x1,y1, x2,y2, x3,y3,x4,y4 = 0,430,250,600, 0,600,0,0
			pdf.setFillColorRGB(0.5,0.,0.)
			p = pdf.beginPath()
			p.moveTo(x1,y1)
			for (x,y) in [(x2,y2), (x3,y3), (x4,y4)]:
				p.lineTo(x,y)
			pdf.drawPath(p, fill=1, stroke=0)


			
			pdf.setFillColorRGB(0.5,0.,0.)
			x1,y1, x2,y2, x3,y3,x4,y4= 600,0,850,180, 850,0,180,0
			p = pdf.beginPath()
			p.moveTo(x1,y1)
			for (x,y) in [(x2,y2), (x3,y3), (x4,y4)]:
				p.lineTo(x,y)
			pdf.drawPath(p, fill=1, stroke=0)
			

				
				

	def tabla(self,pdf,y, profile_id, taller_id):
		profile = Profile.objects.get(id=profile_id)
		self.profile = profile.nombres+' '+profile.apellidos
		estudiante = Estudiante.objects.get(usuario__id__exact= profile.id)

		taller = Taller.objects.get(id=taller_id)
		self.taller = taller
		print(taller)
		pdf.setFont('Helvetica-Bold', 35)
		pdf.setFillColor(black)
		pdf.drawCentredString(415, 400, str(self.profile))

		pdf.setFont('Helvetica-Bold', 35)
		pdf.setFillColorRGB(0.,0.,0.5)
		pdf.drawCentredString(415, 260, str(self.taller))

        
		    
			
			
	def get(self, request, *args, **kwargs):
			profile = self.kwargs.get('profile_id')
			taller = self.kwargs.get('taller_id')
			#producto = Producto.objects.filter(donacion__id__exact=donacion_id)
			
			#Indicamos el tipo de contenido a devolver, en este caso un pdf
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename=Certificado.pdf'
			y = self.tabla

			#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
			buffer = BytesIO()
			#Canvas nos permite hacer el reporte con coordenadas X y Y
			pdf = canvas.Canvas(buffer, pagesize = landscape(A4))
			
			#Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
			self.cabecera(pdf)
			self.tabla(pdf, y, profile, taller)
			#Con show page hacemos un corte de página para pasar a la siguiente
			pdf.showPage()
			pdf.save()
			pdf = buffer.getvalue()
			buffer.close()
			response.write(pdf)
			return response