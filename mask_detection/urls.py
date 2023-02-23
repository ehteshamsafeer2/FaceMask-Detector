
from django.contrib import admin
from django.urls import path
import maskii.views as views
from django.conf import settings #add this
from django.conf.urls.static import static #add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mask_detect, name='mask_detect'),
    path('success', views.success, name='success'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)