from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from student.forms import *
from student.models import *
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            student = authenticate(request, username=username, password=password)
            if student is not None:
                login(request, student)
                return redirect('/')
            else:
                messages.info(request, 'Username OR Password is incorrect')
        context = {}
        return render(request, 'student/login_form.html', context=context)


def registerView(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = StudentRegistrationForm()
        if request.method == 'POST':
            form = StudentRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                student = form.cleaned_data.get('username')
                request.user.studentprofile = request.user
                messages.success(request, 'Accounts was created for '+ student)
                return redirect('student:login')
        context = {
            'form':form
        }
        return render(request, 'student/register_form.html', context=context)


@login_required(login_url='accounts:login')
def logoutView(request):
    if not request.user.is_authenticated:
        return redirect('student:login')
    else:
        logout(request)
        return redirect('/')


@login_required(login_url='student:login')
def updateView(request):
    student = request.user.studentprofile
    form = StudentProfileUpdateForm(instance=student)
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
    context = {
        'form':form,
        'student':student,
    }
    return render(request, 'student/update_form.html', context)


# Having Problem to set the subjects of a student
@login_required(login_url='student:login')
def subjectView(request):
    student = request.user
    form = StudentSubjectForm()
    if request.method == 'POST':
        form = StudentSubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.student = student
            subject.save()
    context = {
        'form':form,
        'student':student,
    }
    return render(request,'student/subjects.html', context)


@login_required(login_url='student:login')
def enterMarks(request,pk):
    student = request.user
    semester = student.semester_set.get(pk=pk)
    form = StudentMarksForm()
    if request.method == 'POST':
        form = StudentMarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.semester = semester
            form.save()
    context = {
        'form':form,
        'student':student
    }
    return render(request, 'student/marks.html', context)


def index(request):
    return render(request, 'student/index.html')
