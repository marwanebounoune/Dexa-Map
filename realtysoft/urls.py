"""realtysoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from quotes.views import serve_protected_document
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('quotation/', include('quotes.urls')),
    path('admin/', admin.site.urls),
    path('map/',include('api_map.urls')),
    path('apis/',include('apis.urls')),
    path('plusInfo/',include('afficher_box_plus_info.urls')),
    path('rapport/',include('afficher_box_rapport.urls')),
    path('filtrageRef/',include('filtrage_ref.urls')),
    path('csv/',include('gestion_csv.urls')),
    path('reference/',include('gestion_ref.urls')),
    path('notes/',include('gestion_commentaires_ref.urls')),
    path('docs/',include('gestion_documents_ref.urls')),
    path('pics/',include('gestion_photos_ref.urls')),
    path('tags/',include('gestion_tags_ref.urls')),
    path('', include('account.urls')),
    path('media/<path:relative_path>', serve_protected_document, name='document-download'),
] 
