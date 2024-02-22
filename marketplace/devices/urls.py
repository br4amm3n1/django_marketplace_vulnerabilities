from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.device_showcase, name='device_showcase'),
    path('devices/<int:device_id>/', views.device_detail, name='device_detail'),
    path('devices/<int:device_id>/create_review/', views.create_review, name='create_review'),
    path('device_reviews/<int:device_id>/', views.show_device_reviews, name='device_reviews'),
    path('devices/categories/', views.show_device_categories, name='device_categories'),
    path('devices/categories/<int:category_id>/', views.show_devices_by_category, name='devices_by_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

