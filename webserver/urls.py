from django.urls import path
from webserver.views import *


urlpatterns = [
	path('', home),
	path('login/', login),
	path('signup/',signup),
	path('dashboard/',dashboard),
	path('certificate/<int:pk>/',certificate),
]