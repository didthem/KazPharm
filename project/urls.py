from django.contrib import admin
from django.urls import path, include
from app import views

from app.views import MyProjLoginView
from app.views import RegisterView, MyProjLogout




urlpatterns = [
    path('admin/', admin.site.urls),
    path('mexel/', views.mexel, name='mexel'),
    path('tumar/', views.tumar, name='tumar'),
    path('alanda/', views.alanda, name='alanda'),
    path('senim/', views.senim, name='senim'),
    path('mua/', views.mua, name='mua'),
    path('city/', views.city, name='city'),
    path('erzh/', views.erzh, name='erzh'),
    path('ymit/', views.ymit, name='ymit'),
    path('zhan/', views.zhan, name='zhan'),
    path('damu/', views.damu, name='damu'),
    path('ansar/', views.ansar, name='ansar'),
    path('profile/', views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),

    path('', views.index, name='index'),
    path('login', views.MyProjLoginView.as_view(), name='login'),
    path('about', views.about, name='about'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('hospital_form/', views.hospital_form_view, name='hospital_form'),
    path('appointment_form/', views.appointment_form_view, name='appointment_form'),
 
]



   


