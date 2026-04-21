
from django.contrib import admin
from django.urls import path, include # Importe o include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eventos.urls')), # Isso conecta a raiz ao app eventos
]
