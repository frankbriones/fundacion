
from django.shortcuts import render, redirect

#https://www.pythoniza.me/hoja-referencia-css3/


# Create your views here.
import time

from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

    
from django.db.models import Count, Q

from comentario.models import Comentario
from persona.models import NID



@login_required
def comentario_list(request):
	msg = None
	
	if 'msg' in request.session:
		msg = request.session['msg']
		del request.session['msg']
	
	template = 'comentario/comentario_list.html'
	comentarios = Comentario.objects.filter(estado=0)

	

	
	print(comentarios)
	data = {
		'comentarios': comentarios,
		'msg2': msg,   
		}
	#print(canT)	
	return render(request, template, data)


@login_required
def comentario_delete (request, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    # comentario.delete()
    comentario.estado = 1
    comentario.save()
    return redirect('comentario-modulo:comentario_list')





	