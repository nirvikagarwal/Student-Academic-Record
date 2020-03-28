from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.models import User
from student.models import StudentProfile, StudentSubject, StudentMarks, AllSubject


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        exclude = ['student']


class StudentSubjectForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(queryset=AllSubject.objects.all(), required=True, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = StudentSubject
        fields = "__all__"
        exclude = ['student',]

class StudentMarksForm(forms.ModelForm):

    class Meta:
        model = StudentMarks
        fields = '__all__'
        exclude = [
            'student',
            'semester',
        ]