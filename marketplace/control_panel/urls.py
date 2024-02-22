from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.view_capabilities, name='view_capabilities'),
    path('reviews/', views.view_reviews, name='view_reviews'),
    path('purchases/', views.view_purchases, name='view_purchases'),
    path('transactions/', views.view_transactions, name='view_transactions'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
