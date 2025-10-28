from django.urls import path
from . import views


urlpatterns = [

    path('registration/Signin',views.signin,name='signin')
   
]
