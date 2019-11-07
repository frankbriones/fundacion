from django.contrib import admin
from django.urls import path, include, re_path

from django.conf.urls import handler404
from django.conf.urls.static import static

from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView

#https://es.stackoverflow.com/questions/930/roles-de-usuarios-en-django

from django.utils.translation import ugettext_lazy as _



urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('/', include(('website.urls', 'website'), namespace='home')),
    path('modulo-donaciones/', include(('donacion.urls', 'donacion'), namespace='donacion')),
    path('modulo-usuario/', include(('persona.urls', 'persona'), namespace='persona')),
    path(
        'talleres/',
        include(('talleres.urls','talleres'),
        namespace='tallers')
        ),
    path(
        'Comments/',
        include(('comentario.urls','comentario'),
        namespace='comentario')
        ),
    path(
        'modulo-programa/',
        include(('programa.urls','programa'),
        namespace='programa')
        ),
    path(
        'modulo-comentario/',
        include(('comentario.urls','comentario'),
        namespace='comentario-modulo')
        ),
    #https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html
    path('accounts/', include('django.contrib.auth.urls')),
    # path('password-reset/',
    #     PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
    #     name='password_reset'),
    # path('password-reset/done/',
    #     PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
    #     name='password_reset_done'),
    # re_path('reset-password/confirm/<uidb64>/<token>/',
    #     PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
    #     name='password_reset_confirm'),
    # path('password-reset/complete/',
    #     PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    #     name='password_reset_complete'),

    path('API/', include(('restapi.urls', 'restapi'), namespace='restapi')),
    
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT)


handler404 = 'donacion.views.error_404_view'

# admin.site.site_header = _("My Site Admin")
# admin.site.site_title = _("My Site Admin")