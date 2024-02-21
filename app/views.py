from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView

from .forms import AuthUserForm, UserProfileForm, RegisterUserForm
from .models import *

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def profile_update(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        # ...обработайте загрузку аватара, если это необходимо
        user.save()
        return redirect('home')  # Перенаправление на страницу профиля
    else:
        return render(request, 'home.html')







def home(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else: 
        form = UserProfileForm(instance=request.user)

    context = {'title': 'Profile', 'form': form}
    return render(request, 'home.html', context)


def index(request):
    return render(request, 'index.html')

def tumar(request):
    return render(request, 'tumar.html')
def alanda(request):
    return render(request, 'alanda.html')
def senim(request):
    return render(request, 'senim.html')
def mua(request):
    return render(request, 'mua.html')
def city(request):
    return render(request, 'city.html')
def erzh(request):
    return render(request, 'erzh.html')
def ymit(request):
    return render(request, 'ymit.html')
def zhan(request):
    return render(request, 'zhan.html')
def damu(request):
    return render(request, 'damu.html')
def mexel(request):
    return render(request, 'mexel.html')
def ansar(request):
    return render(request, 'ansar.html')

def ansar(request):
    return render(request, 'ansar.html')


def about(request):
    return render(request, 'about.html', {'hos': Hospital.objects.all()})



class MyProjLogout(LogoutView):
    next_page = reverse_lazy('login')

class MyProjLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('index')
    def get_success_url(self):
        return self.success_url

class RegisterView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('about')
    success_msg = 'User successfully created'
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("index")
    
def logout_user(request):
    logout(request)
    return redirect("login")

def hospital_form_view(request):
    if request.method == 'POST':
        hospital_id = request.POST.get('hospital_id')
        hospital = get_object_or_404(Hospital, pk=hospital_id)
        doctors = hospital.doctors.all()
        return render(request, 'appointment_form.html', {'hospital': hospital, 'doctors': doctors})
    else:
        return render(request, 'hospital_form.html', {"hospitals": Hospital.objects.all()})

def appointment_form_view(request):
    if request.method == 'POST':
        hospital_id = request.POST.get('hospital_id')
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        time = request.POST.get('time')

        hospital = get_object_or_404(Hospital, pk=hospital_id)
        doctor = get_object_or_404(hospital.doctors, pk=doctor_id)

        appointment = Appointment(user=request.user, hospital=hospital, doctor=doctor, date=date, time=time)
        appointment.save()
        return redirect('about')  # Перенаправление на страницу успешного завершения
    else:
        return HttpResponse('Ошибка: не удалось сохранить запись')  # Измените на свой собственный ответ в случае ошибки

# def doctor_list(request):
#     specializations = Specialization.objects.all()
#     if request.method == 'POST':
#         selected_specialization_id = request.POST.get('specialization')
#         doctors = Doctor.objects.filter(specialization_id=selected_specialization_id)

#         return render(request, 'doctor_list.html', {'specializations': specializations, 'doctors': doctors})

#     return render(request, 'doctor_list.html', {'specializations': specializations})
    
def schedule(request):
    return render(request, 'schedule.html', {'appointments': Appointment.objects.filter(user=request.user)})


# def profile_update(request):
#   user = request.user

#   if request.method == 'POST':
#     form = UserForm(request.POST, request.FILES, instance=user)

#     if form.is_valid():
#       form.save()
#       return redirect('profile')

#   else:
#     form = UserForm(instance=user)

#   return render(request, 'profile_update.html', {'form': form})

