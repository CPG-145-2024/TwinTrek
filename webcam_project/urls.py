"""webcam_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from webcam_app.views import webcam_image_view  # Updated view imports
from django.conf import settings
from django.conf.urls.static import static
from webcam_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/webcam-image/', webcam_image_view, name='webcam-image-view'),  # Updated view reference
    # path('api/webcam-image/<int:image_id>/', get_webcam_image, name='get-webcam-image'),
    path('', TemplateView.as_view(template_name='webcam.html'), name='webcam'),
    path('buggy_feed/',views.buggy_feed,name='buggy_feed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
