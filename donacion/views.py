
from django.shortcuts import render, redirect

#https://www.pythoniza.me/hoja-referencia-css3/


# Create your views here.
import time

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from donacion.models import Donacion, Producto, Tipo, Categoria
from programa.models import Programa, Evento, Detalle
from django.http import JsonResponse
from django.db.models import F, Sum
from django.db.models.aggregates import Count
from persona.models import Profile
from django.template.context_processors import request
from donacion.forms import DonacionForm, ProductoForm
from django.http.response import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest, JsonResponse
from django.urls.base import reverse
from django.views.generic import DetailView, FormView, UpdateView
from persona.models import Persona


def descompuesto(request):
	template = 'donacion/productos_expirados.html'
	x = Producto.objects.filter(fecha_expiracion__range= (datetime.now() - timedelta (days = 365), datetime.now() ))\
				.exclude(tipo__nombre__startswith= 'JUGUETES')\
				.exclude(tipo__nombre__startswith= 'ROPA')\
				.filter(estado=0)
	x = x.filter(condicion=1)


	print(x)
	data ={
	'x': x
	}
	return render(request, template, data)




    
from django.db.models import Count, Q






import json
def chart_data2(request):
    dataset = Producto.objects \
        .values('tipo')\
        .annotate(juguetes=Count('tipo', filter=Q(tipo__nombre__startswith='JUGUETES')))\
        .exclude(tipo__nombre__startswith='MEDICINA')\
        .exclude(tipo__nombre__startswith='ROPA')\
        .exclude(tipo__nombre__startswith='ALIMENTOS')
    dataset2 = Producto.objects \
        .values('tipo')\
        .annotate(medicina=Count('tipo', filter=Q(tipo__nombre__startswith='MEDICINA')))\
        .exclude(tipo__nombre__startswith='JUGUETES')\
        .exclude(tipo__nombre__startswith='ROPA')\
        .exclude(tipo__nombre__startswith='ALIMENTOS')
 
    dataset3 = Producto.objects \
        .values('tipo')\
        .annotate(ropa=Count('tipo', filter=Q(tipo__nombre__startswith='ROPA')))\
        .exclude(tipo__nombre__startswith='JUGUETES')\
        .exclude(tipo__nombre__startswith='MEDICINA')\
        .exclude(tipo__nombre__startswith='ALIMENTOS')

    dataset4 = Producto.objects \
        .values('tipo')\
        .annotate(alimentos=Count('tipo', filter=Q(tipo__nombre__startswith='ALIMENTOS')))\
        .exclude(tipo__nombre__startswith='JUGUETES')\
        .exclude(tipo__nombre__startswith='ROPA')\
        .exclude(tipo__nombre__startswith='MEDICINA')


    juguetes_s = list()
    alimentos_s=list()
    ropa_s = list()
    medicina_s=list()
    for entradaj in dataset:
        juguetes_s.append(entradaj['juguetes'])
        
    for entradam in dataset2:
        medicina_s.append(entradam['medicina'])

    for entradar in dataset3:
        ropa_s.append(entradar['ropa'])


    for entradal in dataset4:
        alimentos_s.append(entradal['alimentos'])


    data = {
    'juguetes_s': json.dumps(juguetes_s),
    'medicina_s': json.dumps(medicina_s),
    'ropa_s': json.dumps(ropa_s),
    
    'alimentos_s': json.dumps(alimentos_s),

    }



    return render(request, 'donacion/chart2.html', data)








def error_404_view(request, exception):
    data = {}
    print(data)
    return render(request,'404.html', data)





def inactivar (request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.estado = 1
    producto.save()
    return HttpResponseRedirect(reverse_lazy('donacion:expira'))


def inactivar2 (request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.estado = 1
    producto.save()
    return HttpResponseRedirect(reverse_lazy('donacion:descompuesto'))

def inactivar3 (request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.estado = 1
    producto.save()
    return HttpResponseRedirect(reverse_lazy('donacion:stock_total'))




@login_required
def show_donacion(request, donacion_id):
	template = 'donacion/show/show_donacion.html'
	donacion = Donacion.objects.get(id=donacion_id)
	print(donacion.id)
	productos = Producto.objects.filter(donacion__id__exact=donacion_id)

	canti = productos.aggregate(suma = Sum('cantidad'))

	data = {
	'donacion': donacion,
	'productos': productos,
	'cantidad': canti	
	}
	return render(request, template, data)




@login_required
def edit(request, donacion_id):
	template = 'donacion/detalle_donacion.html'
	donacion = Donacion.objects.get(id=donacion_id)
	
	

	productos = Producto.objects.filter(donacion__id__exact=donacion_id)

	canti = productos.aggregate(suma = Sum('cantidad'))
	#print(canti)
	data = {
		
		'productos': productos,
		'canti': canti,
		'donacion': donacion,
	}
	return render(request, template, data)






from datetime import timedelta
import time
from django.http import JsonResponse
import json
@login_required
def productos_expiran (request, *args, **kwargs):
	m = None
	if 'm' in request.session:
		m = request.session['m']
		del request.session['m']
	template = 'donacion/productos_expiran.html'
	#date = time.strftime("%Y-%m-%d")
	productos = Producto.objects.filter(fecha_expiracion__range= ( datetime.now() , datetime.now() + timedelta (days=90)))\
				.exclude(tipo__nombre__startswith= 'JUGUETES')\
				.exclude(tipo__nombre__startswith= 'ROPA')
	productos = productos.filter(estado=0)

	# f = Producto.objects.filter(fecha_expiracion__range= (datetime.now() - timedelta (days = 60), datetime.now() - timedelta (days=1)))\
	# 			.exclude(tipo__nombre__startswith= 'JUGUETES')\
	# 			.exclude(tipo__nombre__startswith= 'ROPA')
	# f = f.filter(estado=0)
	# for x in f:
	# 	if x.fecha_expiracion > (datetime.now().date() - timedelta(days=60)) and x.fecha_expiracion < (datetime.now().date()):
	# 		request.session['m'] = "Alerta"
			
	# 		if x.stock > 0 :
	# 			print(x)
			

	
	#stock = []

	for producto in productos:
		

		id_total = Detalle.objects.filter(producto__id=producto.id)
		j = id_total.aggregate(suma = Sum('cant'))
		if j['suma'] is None:
			j['suma'] = 0
			producto.stock = producto.cantidad
		#producto.add(stock = (j['suma']))
		else:
			producto.stock = int(j['suma'])
			producto.stock = producto.cantidad - producto.stock
		
		producto.save()
		
	
		

	data = {
	'productos': productos,
	'm': m,

	#'j': j['suma']
	#'j': j['x'],

	#'date': date,
	}
	return render(request,template, data)








import datetime
import time

@login_required
def donacion(request):
	

	m = None
	if 'm' in request.session:
		m = request.session['m']
		del request.session['m']
	
	template = 'donacion/donacion_list.html'
	cant = Producto.objects.aggregate(suma = Sum('cantidad'))
	cantR =  Producto.objects.filter( tipo__nombre__startswith = "ROPA").aggregate(suma = Sum('cantidad'))
	cantM =  Producto.objects.filter(tipo__nombre__startswith = "MEDICINA").aggregate(suma = Sum('cantidad'))
	cantA =  Producto.objects.filter(tipo__nombre__startswith = "ALIMENTOS").aggregate(suma = Sum('cantidad'))
	cantJ =  Producto.objects.filter(tipo__nombre__startswith = "JUGUETES").aggregate(suma = Sum('cantidad'))
	#cantJ = Donacion.objects.filter(donacion__tipo = 3).aggregate(suma = Sum('cantidad'))
	date = time.strftime("%Y")
	donaciones = Donacion.objects.filter(created__gte =  time.strftime('%Y-1-1'),
										created__lte = time.strftime('%Y-12-31')  )

	f = Producto.objects.filter(fecha_expiracion__range= (datetime.now() - timedelta (days = 360), datetime.now()))\
				.exclude(tipo__nombre__startswith= 'JUGUETES')\
				.exclude(tipo__nombre__startswith= 'ROPA')\
				.filter(estado=0)


	
	
	for x in f:
		print()
		fecha_actual = datetime.now().date()
		print(x.stock)
		
		if x.stock == 0 :
			x.estado = 1
			x.save()
		if  x.fecha_expiracion < fecha_actual and x.stock > 0:
				x.condicion = 1
				x.save(update_fields=['condicion'])
				request.session['m'] = "Alerta"
				print(m)
				if x.stock == 0 :
					x.estado = 1
					x.save()


	#print(expirar)
	data = {
		'date': date,
		'cant': cant,
		'cantR': cantR,
        'cantM': cantM,
        'cantA': cantA,
        'cantJ': cantJ,
		'donaciones': donaciones,
		'm': m
		}
	#print(canT)	
	return render(request, template, data)





from django.forms import modelformset_factory
@login_required
def nuevaDonacion(request):
	template = 'donacion/nueva_donacion.html'
	form = DonacionForm(request.POST)
	user = request.user
	print(user)
	if form.is_valid() :
			donacion = form.save(commit=False)
			donacion.usuario = user
			donacion.save()

			slug = donacion.pk
			
			request.session['msg'] = "Ingreso de Donacion Excitosa (agregar productos o salir, con el boton listo)"
			return redirect('donacion:producto', slug)
		
	data = { 
			'form': form
			
		}
	return render(request, template, data)









@login_required
def producto(request, slug):
	msg = None
	
	if 'msg' in request.session:
		msg = request.session['msg']
		del request.session['msg']
	template = 'donacion/nueva_producto.html'
	donacion = Donacion.objects.get(id=slug)
	form = ProductoForm()
	productos = Producto.objects.filter(donacion__id__exact=slug).order_by('tipo')
	canti = productos.aggregate(suma = Sum('cantidad'))
	slug = slug

	if request.method == 'POST':
		form = ProductoForm(request.POST, request.FILES)
		form.modificarQuerySet(request.POST["tipo"])

		if form.is_valid():
			form = Producto(donacion=donacion, 
				
				descripcion = form.cleaned_data['descripcion'],
				fecha_expiracion = form.cleaned_data['fecha_expiracion'],
				tipo = form.cleaned_data['tipo'],
				categoria = form.cleaned_data['categoria'],
				cantidad = form.cleaned_data['cantidad']
			)
			form.save()
			request.session['msg'] = "Ingreso de mas Productos"
			return redirect('donacion:producto', slug)	

	#lista de productos para la donacion
	productos = Producto.objects.filter(donacion_id=donacion.id)
	
	
	#stock = []

	for producto in productos:
		print(producto)
		id_total = Detalle.objects.filter(producto__id=producto.id)
		j = id_total.aggregate(suma = Sum('cant'))
		if j['suma'] is None:
			j['suma'] = 0
			producto.stock = producto.cantidad
		#producto.add(stock = (j['suma']))
		else:
			producto.stock = int(j['suma'])
			producto.stock = producto.cantidad - producto.stock
		
		producto.save()

	data = {
		'form':form ,
		'donacion': donacion,
		'productos': productos,
		'canti': canti,
		'msg': msg,
		
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


#pdf para mmostrar los detalles de la donacioin

class ReporteDonacionPDF(View):  

     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.jpg que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/imagenes/logos.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 30, 700, 200, 150,preserveAspectRatio=True)
        pdf.setFont("Helvetica", 20)
        pdf.drawString(250, 790, u"'Fundacion Tacita Calietne'")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(300, 770, u"Detalle Donacion")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(380, 710, u"Fecha: --------")
        pdf.drawString(25, 670, u"La Fundaion Tacita Caliente, realiza el evento _________, el cual tendra la salida de los siguientes")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(25, 650, u"Productos que se encuentra detallados acontinuacion inventario, autorizado por la administracion de la Instituion.")
        pdf.setFont("Helvetica", 11)
        pdf.setFont("Helvetica", 12) 
        pdf.drawString(350, 50, u"Firma: _______________________")

    def tabla(self,pdf,y, donacion_id):
        #Creamos una tupla de encabezados para neustra tabla
        

        donacion = Donacion.objects.get(id= donacion_id)
        producto = Producto.objects.filter(donacion__id__exact=donacion_id)

        encabezados = ( 'Tipo Producto', 'Producto', 'Fecha Expira', 'Cantidad')
        #print(taller.descripcion)
        altX = 600
        

        detalles = [( producto.tipo.nombre, producto.descripcion, producto.fecha_expiracion, producto.cantidad)
        for producto in producto ]
        for detalle in detalles:
        	altX = altX - 18
        	
        if producto :		

	        #Establecemos el tamaño de cada una de las columnas de la tabla
	        
	        detalle_orden = Table([encabezados] + detalles, colWidths=[ 5 * cm, 5 * cm, 5* cm, 2 * cm])

	        #Aplicamos estilos a las celdas de la tabla
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
	        
	        #Establecemos el tamaño de la hoja que ocupará la tabla 
	        detalle_orden.wrapOn(pdf, 800, 600)
	        #Definimos la coordenada donde se dibujará la tabla
	        detalle_orden.drawOn(pdf, 60, altX)
	        print(altX)
		    

		         
    def get(self, request, *args, **kwargs):
    	donacion = self.kwargs.get('donacion_id')
    	response = HttpResponse(content_type='application/pdf')
    	response['Content-Disposition'] = 'inline; filename=Detalles_donacion.pdf'
    	buffer = BytesIO()
    	pdf = canvas.Canvas(buffer)
    	self.cabecera(pdf)
    	y = self.tabla
    	self.tabla(pdf, y, donacion)
    	pdf.showPage()
    	pdf.save()
    	pdf = buffer.getvalue()
    	buffer.close()
    	response.write(pdf)
    	return response








def stock_total(request):
	msg2 = None
	if 'msg2' in request.session:
		msg2 = request.session['msg2']
		del request.session['msg2']
	template = 'donacion/stock.html'
	#date = time.strftime("%Y-%m-%d")
	productos = Producto.objects.all()
	productos = productos.filter(estado=0)
	fecha_actual = datetime.now().date()
	
	#stock = []

	for producto in productos:
		print(producto)
		id_total = Detalle.objects.filter(producto__id=producto.id)
		j = id_total.aggregate(suma = Sum('cant'))

		if producto.fecha_expiracion < fecha_actual and producto.stock > 0:
			producto.condicion = 1
			producto.save(update_fields=['condicion'])
		if j['suma'] is None:
			j['suma'] = 0
			producto.stock = producto.cantidad
		#producto.add(stock = (j['suma']))
		else:
			producto.stock = int(j['suma'])
			producto.stock = producto.cantidad - producto.stock
		
		producto.save()
		print(producto.stock)

	expirar = Producto.objects.filter(fecha_expiracion__range= (datetime.now(),  datetime.now() + timedelta (days = 90)))
	expirar = expirar.filter(estado = 0)
	

	for x in expirar:
		if x :
			
			request.session['msg2'] = "Productos proximos a expirar!!!!..."
		else:
			request.session['msg2'] = ""
			
	
	
		

		

	data = {
	'productos': productos,
	'expirar': expirar,
	'msg2': msg2
	#'j': j['x'],

	#'date': date,
	}
	return render(request,template, data)













@login_required
def reportes(request):
	template = 'Reportes/reporte_base.html'
	date = time.strftime('%Y')
	return render(request ,template, {'date': date,})



import time
from datetime import datetime



from talleres.models import Taller
def reporte_talleres(request):
	template = 'donacion/show/show_reporte_taller.html'
	date = time.strftime("%d/%B/%Y")
	talleres = Taller.objects.all()
	query = ''
	query2 = ''
	if 'query' and 'query2' in request.GET:
		query1 = time.strftime(request.GET['query'])
		# query2 = (datetime.strptime(query1, '%Y-%m-%d') + timedelta( days= 30))
		query2 = time.strftime(request.GET['query2'])
		talleres = talleres.filter(fecha_inicio__range=(query1, query2  ))
		print(talleres)

	data = {
	'query1': query1,
	'talleres': talleres,
	'date': date  
	}
	return render(request, template, data)




def reporte_voluntarios(request):
	template = 'donacion/show/show_reporte_voluntario.html'
	date = time.strftime("%d/%B/%Y")
	voluntarios = Persona.objects.filter(estado = 0).order_by('nombres')
	query = ''
	query2 = ''
	if 'query' and 'query2' in request.GET:
		query1 = time.strftime(request.GET['query'])
		# query2 = (datetime.strptime(query1, '%Y-%m-%d') + timedelta( days= 30))
		query2 = time.strftime(request.GET['query2'])
		voluntarios = voluntarios.filter(created__range=(query1, query2  ))
		print(voluntarios )
        

	data = {
	'voluntarios': voluntarios,
	'date': date  
	}
	return render(request, template, data)


def reporte_donaciones(request):
	template = 'donacion/show/show_reporte_donacion.html'
	date = time.strftime("%d/%B/%Y")
	#donaciones = Producto.objects.filter(estado = 0).order_by('tipo')
	donaciones = Producto.objects.order_by('tipo')
	query = ''
	query2 = ''
	if 'query' and 'query2' in request.GET:
		query1 = time.strftime(request.GET['query'])
		query2 = time.strftime(request.GET['query2'])
		donaciones = donaciones.filter(fecha_expiracion__range=(query1, query2  ))
		print(donaciones)
        	

	data = {
	'donaciones': donaciones,
	'date': date , 
	'query1': query1,
	'query2': query2
	}
	
	return render(request, template, data)


from programa.models import Programa
def reporte_programas(request):
	template = 'donacion/show/show_reporte_programa.html'
	date = time.strftime("%d/%B/%Y")
	date1 = time.strftime("%Y")

	programas = Programa.objects.filter(estado = 0)
	query = ''
	query2 = ''
	if 'query' and 'query2' in request.GET:
		query1 = time.strftime(request.GET['query'])
		# query2 = (datetime.strptime(query1, '%Y-%m-%d') + timedelta( days= 30))
		query2 = time.strftime(request.GET['query2'])
		programas = programas.filter(fecha_programa__range=(query1, query2  ))
		print(programas)
        

	data = {
	'programas': programas,
	'date': date,
	'date1': date1,
	'query1': query1,  
	}
	return render(request, template, data)












def consultarCategoriasAsJson(request):
	if request.method == 'POST' and "tipo_id" in request.POST:
		tipo_id = request.POST["tipo_id"]
		if tipo_id not in ('', None):
			categorias = Categoria.objects.filter(tipo__id__exact = tipo_id).order_by('categoria')
			categorias = categorias.order_by('categoria')							
			return JsonResponse([{'id':'', 'categoria':'---Escoger una Categoria---'}] + [{'id': x.id, 'categoria':x.categoria} for x in categorias], safe=False)
		else:
			return JsonResponse([{'id':'', 'categoria':'-Escoger una categorias-'}], safe=False)
	else:
		return HttpResponseBadRequest("Se ha realizado un mal requerimiento")

