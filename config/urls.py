# GPT-5.5 assisted in the writing of this code

"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from photoapp.views import SignUpView

urlpatterns = [
    # authentication endpoints are provided by Django's mature,security reviewed  auth views rather than hand rolled, this gives login and logout url names
    path('accounts/', include('django.contrib.auth.urls')),

    # Registration is the one auth view Django does not ship, so I added it
    path('accounts/signup/', SignUpView.as_view(), name='signup'),

    # Main app
    path('', include('photoapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
