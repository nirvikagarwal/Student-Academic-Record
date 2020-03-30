from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from student.forms import *
from student.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
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
            form.save_m2m()
    context = {
        'form':form,
        'student':student,
    }
    return render(request,'student/subjects.html', context)


def cal_cgpa(student,semester):
    student_subject = get_object_or_404(StudentSubject, student=student, semester=semester)
    all_subjects = AllSubject.objects.filter(studentsubject=student_subject)
    total_credits = 0
    credit_points = 0
    points = 0
    for subject in all_subjects:
        marks = StudentMarks.objects.get(student=student, semester=semester, subject=subject)
        if marks.marks >=90:
            points = 10
        elif marks.marks >=80:
            points = 9
        elif marks.marks >=70:
            points = 8
        elif marks.marks >=60:
            points = 7
        elif marks.marks >=50:
            points = 6
        elif marks.marks >=40:
            points = 5
        elif marks.marks >=30:
            points = 4
        credit_points = credit_points + (points*subject.credit_points)
        total_credits = total_credits + subject.credit_points
    cgpa = credit_points/total_credits
    return cgpa

        
@login_required(login_url='student:login')
def enterMarks(request,pk):
    student = request.user
    semester = AllSemester.objects.get(pk=pk)
    student_subject = get_object_or_404(StudentSubject, student=student, semester=semester)
    # all_subjects = AllSubject.objects.filter(studentsubject=student_subject)
    subject_count = AllSubject.objects.filter(studentsubject=student_subject).count()
    MarksFormSet = inlineformset_factory(User, StudentMarks,fields=('semester','subject','marks'), extra=subject_count)
    # form = StudentMarksForm() 
    formset = MarksFormSet(initial = [{'semester':semester,}])
    if request.method == 'POST':
        # form = StudentMarksForm(request.POST)
        formset = MarksFormSet(request.POST, instance=student)
        if formset.is_valid():
            formset.save(commit=False)
            # for each inline element I want to save the semester field to the current semester
            for form in formset:
                form.semester = semester
                formset.save()
            formset.save()
            cgpa = cal_cgpa(student,semester)
            student_cgpa = Cgpa(student=student, semester=semester, cgpa=cgpa)
            student_cgpa.save()
            return redirect('/')

    context = {
        'formset':formset,
        'student':student,
        # 'all_subjects':all_subjects,
    }
    return render(request, 'student/marks.html', context)






def index(request):
    return render(request, 'student/index.html')
