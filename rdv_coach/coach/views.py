# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth import login, authenticate, logout
from datetime import datetime, timedelta
from .forms import Appointment
from django.contrib import messages
from datetime import datetime
#from .forms import LoginForm
# Views

 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #first_name = form.cleaned_data.get('First name')
            # last_name = form.cleaned_data.get('Last name')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('booking')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



def logout_view(request):
    logout(request)
    message = ' You are deconnected'
    return redirect('home')




def login_view(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None and user.username=='AhmadDarwiche1992':
                login(request, user)
                return redirect('staffPanel')
            if user is not None:
                login(request, user)
                return redirect('booking')
        message = 'Identifiants invalides.'
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, "home.html" )

def booking(request):
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        if service == None:
            messages.success(request, "Please Select A Service!")
            return redirect('booking')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('bookingSubmit')


    return render(request, 'booking.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
        })

def bookingSubmit(request):
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    #Get stored data from django session:
    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before:
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1:
                            AppointmentForm = Appointment.objects.get_or_create(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            )
                            messages.success(request, "Appointment Saved!")
                            return redirect('home')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")


    return render(request, 'bookingSubmit.html', {
        'times':hour,
    })

def userPanel(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user':user,
        'appointments':appointments,
    })

def userUpdate(request, id):
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    #Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    #24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('userUpdateSubmit', id=id)


    return render(request, 'userUpdate.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'delta24': delta24,
            'id': id,
        })

def userUpdateSubmit(request, id):
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            AppointmentForm = Appointment.objects.filter(pk=id).update(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "Appointment Edited!")
                            return redirect('home')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")
        return redirect('userPanel')


    return render(request, 'userUpdateSubmit.html', {
        'times':hour,
        'id': id,
    })

def staffPanel(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    #Only show the Appointments 21 days from today
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'staffPanel.html', {
        'items':items,
    })

def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def validWeekday(days):
    #Loop days you want in the next 21 days:
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays
    
def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def checkTime(times, day):
    #Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x
