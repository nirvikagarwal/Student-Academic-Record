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


# Login View
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


# For Registration
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


# Updates the Student Profile
@login_required(login_url='student:login')
def updateView(request):
    student = request.user.studentprofile
    form = StudentProfileUpdateForm(instance=student)
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form':form,
        'student':student,
    }
    return render(request, 'student/update_form.html', context)


# Function for calculating the CGPA
def cal_cgpa(student):
    allSgpa = Sgpa.objects.filter(student=student)
    semesters = Sgpa.objects.filter(student=student).count()
    total = 0
    for sgpa in allSgpa:
        total += sgpa.sgpa
    cgpa = total/semesters
    return cgpa
 

 # Function for calculating SGPA
def cal_sgpa(student,semester):
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
    sgpa = credit_points/total_credits
    return sgpa


# Function for storing the subjects of a student each semester
@login_required(login_url='student:login')
def subjectView(request):
    student = request.user
    semesters = StudentSubject.objects.filter(student=student)
    subjects = StudentSubject.objects.filter(student=student)
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
        'semesters':semesters,
        'subjects':subjects,
        'subject_list':subject_list,
    }
    return render(request,'student/subjects.html', context)


# Function for entering the marks 
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
            sgpa = cal_sgpa(student,semester)
            student_sgpa = Sgpa(student=student, semester=semester, sgpa=sgpa)
            student_sgpa.save()
            cgpa = cal_cgpa(student)
            student_cgpa = Cgpa.objects.get(student=student)
            student_cgpa.cgpa = cgpa
            student_cgpa.save()

            return redirect('/')

    context = {
        'formset':formset,
        'student':student,
        # 'all_subjects':all_subjects,
    }
    return render(request, 'student/marks.html', context)


@login_required(login_url='student:login')
def selectSemester(request):
    student = request.user
    semesters = StudentSubject.objects.filter(student=student).count()
    semester_list = AllSemester.objects.all()[:semesters]
    context = {
        'semester_list':semester_list,
    }
    return render(request, 'student/select_semester.html', context)

@login_required(login_url='student:login')
def index(request):
    student = request.user
    cgpa = Cgpa.objects.get(student=student)
    semester_count = StudentSubject.objects.filter(student=student).count() + 1
    present_semester = AllSemester.objects.get(pk=semester_count)
    sgpa_list = Sgpa.objects.filter(student=student)

    context = {
        'student':student,
        'cgpa':cgpa,
        'present_semester':present_semester,
        'sgpa_list':sgpa_list,
    }
    return render(request, 'student/index.html',context)
