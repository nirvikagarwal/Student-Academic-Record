from django.shortcuts import render
from django.contrib.auth import (
                            authenticate,
                            login,
                            logout,
                            )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from student.forms import StudentLoginForm, StudentRegistrationForm, StudentProfileUpdateForm
from student.models import User

# Create your views here.

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = StudentLoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            student = authenticate(email=email, password=password)
            login(request,student)
            return redirect('home')
            context = {
                'form':form
            }
        
        return render(request, 'student/login_form.html', context=context)


def registerView(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = StudentRegistrationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            student = form.save(commit=True)
            # password = form.cleaned_data.get('password1')
            # student.set_password(password)
            # student.save()
        new_student = authenticate(email=student.email, password=password1)
        login(request,new_student)

    context = {
        'form':form
    }
    return render(request, 'student/register_form.html', context=context)


def logoutView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        logout(request)
        return redirect('home')

@login_required()
def updateView(request):
    student = get_object_or_404(User, pk=request.user.pk)
    form = StudentProfileUpdateForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save(commit=True)
        return redirect('home')
    
    context={
        'form':form
    }
    return render(request, 'student/update_form.html', context)
