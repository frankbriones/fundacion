from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from donacion.models import Donacion, Producto, Tipo
from django.http import JsonResponse
from django.db.models import F, Sum
from django.db.models.aggregates import Count
from persona.models import Profile
from django.template.context_processors import request
from donacion.forms import DonacionForm, ProductoForm
from programa.forms import ProgramaForm, DetalleForm, EventoForm
from django.http.response import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest, JsonResponse
from django.urls.base import reverse
from django.views.generic import DetailView, FormView, UpdateView
from persona.models import Persona
from django.shortcuts import render, redirect
from programa.models import Programa, Detalle, Evento

import time
import datetime

from rest_framework.decorators import  api_view
from rest_framework.response import  Response


from programa.serializers import ProgramaSerializer
@api_view(['GET'])
def list_programas(request):
	programas = Programa.objects.all()
	#fecha_actual = datetime.now().date()
	serializer = ProgramaSerializer(programas, many=True)
	return Response(serializer.data)


















#https://www.pythoniza.me/hoja-referencia-css3/
# Create your views here.
import time
import datetime

@login_required
def agregar_detalle(request, slug):
	msg = None
	if 'msg' in request.session:
		msg = request.session['msg']
		del request.session['msg']
	template = 'programa/nuevo_prod_programa.html'
	programa = Programa.objects.get(id=slug)

	#max_stock = producto.stock
	form = DetalleForm()

	
	detalle = Detalle.objects.filter(programa__id__exact=programa.id)
	if request.method == 'POST':
		form = DetalleForm(request.POST, request.FILES)
		form.modificarQuerySet(request.POST["tipo"], request.POST["categoria"])
		if form.is_valid():
			form = Detalle(programa=programa, 
				tipo = form.cleaned_data['tipo'],
				producto = form.cleaned_data['producto'],
				cant = form.cleaned_data['cant'],
				usuario = request.user, 
			)
			pk = form.producto
			pk.stock = pk.stock - form.cant
			pk.save()
			form.save()


			
			

			request.session['msg'] = "Registro de producto correcto"
			return redirect('programa:agregar_detalle', slug)
	else:
		form = DetalleForm()

	data = {
		'form':form ,
		'programa': programa,
		'totals':  detalle,	
		'msg3': msg,
    }
	return render(request, template, data)







@login_required
def editaPrograma(request, programa_id):
	template = 'programa/detalle_programa.html'
	programa = Programa.objects.get(id=programa_id)
	total = Detalle.objects.filter(programa__id__exact=programa_id)
	canti = total.aggregate(suma = Sum('cant'))
	#print(total)
	data ={
		'programa': programa,
		'totals': total,
		'canti': canti
	}
	return render(request ,template, data)



@login_required
def programa(request):
	
	msg = None
	if 'msg' in request.session:
		msg = request.session['msg']
		del request.session['msg']
	
	
	template = 'programa/programa_list.html'
	cant = Detalle.objects.aggregate(suma = Sum('cant'))

	cantR = Detalle.objects.filter(producto__condicion=0).filter(tipo__nombre__startswith = "ROPA").aggregate(suma = Sum('cant'))
	cantM = Detalle.objects.filter(producto__condicion=0).filter(tipo__nombre__startswith = "MEDICINA").aggregate(suma = Sum('cant'))
	cantA = Detalle.objects.filter(producto__condicion=0).filter(tipo__nombre__startswith = "ALIMENTOS").aggregate(suma = Sum('cant'))
	cantJ = Detalle.objects.filter(producto__condicion=0).filter(tipo__nombre__startswith = "JUGUETES").aggregate(suma = Sum('cant'))

	cantRp =  Producto.objects.filter(estado=0).filter(tipo__nombre__startswith = "ROPA").aggregate(suma = Count('id'))
	cantMp =  Producto.objects.filter(estado=0).filter(tipo__nombre__startswith = "MEDICINA").aggregate(suma = Count('id'))
	cantAp =  Producto.objects.filter(estado=0).filter(tipo__nombre__startswith = "ALIMENTOS").aggregate(suma = Count('id'))
	cantJp =  Producto.objects.filter(estado=0).filter(tipo__nombre__startswith = "JUGUETES").aggregate(suma = Count('id'))
	print(cantMp)
	
	cantB = Producto.objects.filter(estado=0).aggregate(suma = Sum('cantidad'))
	print(cantB)
	
	date = time.strftime("%Y")

	if cant['suma'] and cantB['suma'] is not 0:
		import math 
		stck = int(cantB['suma']) - int(cant['suma'])
		stck = int(math.fabs(stck))
	else:
		stck = 0


	programas = Programa.objects.filter(estado=0)
	from datetime import date
	fecha = date.today()
	print(fecha)


	for p in programas:
		if p.fecha_culminacion < fecha:
			p.estado = 1

			p.save()
			
		
		
		
		

		

	data = {
		'date': date,
		'cant': cant,
		'programas': programas,
		'cantR': cantR,
		'cantM': cantM,
		'cantA': cantA,
		'cantJ': cantJ,
		'cantRp': cantRp,
		'cantMp': cantMp,
		'cantAp': cantAp,
		'cantJp': cantJp,
		'msg': msg,
		'cantB': cantB,
		'stck': stck
		}
		
	return render(request, template, data)



@login_required
def nuevoPrograma(request):
	template = 'programa/nuevo_programa.html'
	form = ProgramaForm()
#	TotalFormSet = modelformset_factory(
#		Total,
#		fields = ( 'tipo', 'producto', 'cant'),
#		extra=1,
#		)
	if request.method == 'POST':
		form = ProgramaForm(request.POST, request.FILES)
#		formset = TotalFormSet(request.POST, request.FILES)

		if form.is_valid():
			programa = form.save(commit = False)
			programa.save()
#			for e in formset:
#				try:
#					total = Total(programa=programa, 
#						tipo = e.cleaned_data['tipo'],
#						producto = e.cleaned_data['producto'],
#						cant = e.cleaned_data['cant']) 
#					total.save()
			request.session['msg'] = "Evento Registrado Excitosamente"
			slug = programa.pk

			return redirect('programa:agregar_detalle', slug)
#				except Exception as e:
#					break
	else:
		form = ProgramaForm()
#		formset = TotalFormSet(queryset=Producto.objects.none())
	data = { 
		'form': form,
#		'formset': formset,
	}
	return render(request, template, data)






@login_required
def nuevoEvento(request):
	template = 'programa/nuevo_evento.html'
	form = EventoForm()
#	TotalFormSet = modelformset_factory(
#		Total,
#		fields = ( 'tipo', 'producto', 'cant'),
#		extra=1,
#		)
	if request.method == 'POST':
		form = EventoForm(request.POST, request.FILES)
#		formset = TotalFormSet(request.POST, request.FILES)

		if form.is_valid():
			programa = form.save(commit = False)
			programa.save()
#			for e in formset:
#				try:
#					total = Total(programa=programa, 
#						tipo = e.cleaned_data['tipo'],
#						producto = e.cleaned_data['producto'],
#						cant = e.cleaned_data['cant']) 
#					total.save()
			request.session['msg'] = "Nuevo Programa"
			return redirect('programa:programas')
#				except Exception as e:
#					break
	else:
		form = EventoForm()
#		formset = TotalFormSet(queryset=Producto.objects.none())
	data = { 
		'form': form,
#		'formset': formset,
	}
	return render(request, template, data)
















# Create your views here.
def inactivar_evento (request, evento_id):
   
    evento = Evento.objects.get(id=evento_id)
    evento.estado = 1
    evento.save()
    return HttpResponseRedirect(reverse('programa:lista_programas'))





@login_required
def lista_programas(request):
    template = 'programa/programas_list.html'
    eventos = Evento.objects.filter(estado=0).order_by('nombre')
    
    #print(personas)
    data ={
    'eventos': eventos,
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


class ReporteProgramaPDF(View):  

     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.jpg que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/imagenes/logos.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 30, 700, 200, 150,preserveAspectRatio=True)
        pdf.setFont("Helvetica", 20)
        pdf.drawString(250, 790, u"'Fundacion Tacita Calietne'")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(300, 770, u"Detalle del Pedido")
        pdf.setFont("Helvetica", 12)
        
        pdf.drawString(350, 50, u"Firma: _______________________")

    def tabla(self,pdf,y, programa_id):
        #Creamos una tupla de encabezados para neustra tabla
        date = time.strftime("%d/%b/%Y")
        evento = Programa.objects.get(id=programa_id)
        self.evento = evento
        
        self.fecha_inicio = evento.fecha_programa
        print(self.fecha_inicio)
        pdf.drawString(360, 700, ("Fecha de hoy : " + date))
        pdf.setFont("Helvetica", 12)
        pdf.drawString(25, 700, ("Descripcion del Evento : " + str(self.evento)))
        pdf.setFont("Helvetica", 12)
        pdf.drawString(25, 680, ("Fecha del evento: " + str(self.fecha_inicio)))
        pdf.setFont("Helvetica", 11)
        pdf.drawString(25, 630, ("La Fundaion Tacita Caliente realiza un evento, el cual tendra como pedido los siguientes"))
        pdf.setFont("Helvetica", 11)
        pdf.drawString(25, 610, u"Productos que se encuentra detallados acontinuacion. Inventario, autorizado por la administracion ")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(25, 590, u"de la Institucion. ")
        pdf.setFont("Helvetica", 11)
        
        programa = Programa.objects.get(id= programa_id)
        producto = Detalle.objects.filter(programa__id__exact=programa_id)

        encabezados = ('Tipo Producto', 'Producto', 'Categoria', 'Cant.', 'Descripcion')
        #print(taller.descripcion)
        altX = 560

        detalles = [( producto.tipo.nombre, producto.producto.descripcion, producto.producto.categoria, producto.cant)
        for producto in producto ]
        for detalle in detalles:
        	altX = altX - 18
        	
        if producto :		

	        #Establecemos el tamaño de cada una de las columnas de la tabla
	        
	        detalle_orden = Table([encabezados] + detalles, colWidths=[ 4 * cm, 4 * cm, 4* cm, 1* cm, 4 * cm])

	        #Aplicamos estilos a las celdas de la tabla
	        detalle_orden.setStyle(TableStyle(
	            [
	                #La primera fila(encabezados) va a estar centrada
	                ('ALIGN',(0,0),(3,0),'CENTER'),
	                #Los bordes de todas las celdas serán de color azul y con un grosor de 1
	                ('GRID', (0, 0), (-1, -1), 0.2, colors.blue), 
	                #El tamaño de las letras de cada una de las celdas será de 10
	                ('FONTSIZE', (0, 0), (-1, -1), 10),
	            ]
	        ))
	        
	        #Establecemos el tamaño de la hoja que ocupará la tabla 
	        detalle_orden.wrapOn(pdf, 800, 600)
	        #Definimos la coordenada donde se dibujará la tabla
	        detalle_orden.drawOn(pdf, 30, altX)
	        print(altX)
		    

		         
    def get(self, request, *args, **kwargs):
    	programa = self.kwargs.get('programa_id')
    	response = HttpResponse(content_type='application/pdf')
    	response['Content-Disposition'] = 'inline; filename=Detalles_programa.pdf'
    	buffer = BytesIO()
    	pdf = canvas.Canvas(buffer)
    	self.cabecera(pdf)
    	y = self.tabla
    	self.tabla(pdf, y, programa)
    	pdf.showPage()
    	pdf.save()
    	pdf = buffer.getvalue()
    	buffer.close()
    	response.write(pdf)
    	return response






from donacion.models import Categoria




def consultarCategoriasAsJson(request):
	if request.method == 'POST' and "tipo_id" in request.POST:
		tipo_id = request.POST["tipo_id"]
		if tipo_id not in ('', None):
			categorias = Categoria.objects.filter(tipo__id__exact = tipo_id).order_by('categoria')
			categorias = categorias.order_by('categoria')							
			return JsonResponse([{'id':'', 'categoria':'---Escoger una Categoria---'}] + [{'id': x.id, 'categoria':x.categoria} for x in categorias], safe=False)
		else:
			return JsonResponse([{'id':'', 'categoria':'-Escoger una categoria-'}], safe=False)
	else:
		return HttpResponseBadRequest("Se ha realizado un mal requerimiento")



def consultarProductosAsJson(request):
    if request.method == 'POST' and "categoria_id" in request.POST:
        categoria_id = request.POST["categoria_id"]
        if categoria_id not in ('', None):
            productos = Producto.objects.filter(categoria__id__exact = categoria_id).order_by('descripcion')
            productos = productos.filter(estado=0)
            return JsonResponse([{'id':'', 'descripcion':'---Escoger un producto---'}] + [{'id': producto.id, 'descripcion':producto.descripcion} for producto in productos], safe=False)
        else:
            return JsonResponse([{'id':'', 'descripcion':'-Escoger un producto-'}], safe=False)
    else:
        return HttpResponseBadRequest("Se ha realizado un mal requerimiento")


