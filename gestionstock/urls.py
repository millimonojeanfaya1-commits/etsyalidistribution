"""
URL configuration for gestionstock project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('fournisseurs/', include('fournisseurs.urls')),
    path('ventes/', include('ventes.urls')),
    path('credits/', include('credits.urls')),
    path('stocks/', include('stocks.urls')),
    path('parc-motorise/', include('parc_motorise.urls')),
    path('personnel/', include('personnel.urls')),
    path('charges/', include('charges.urls')),
    path('profits/', include('profits.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
