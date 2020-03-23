from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget
from student.models import User


class StudentLoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     if email and password:
    #         student = authenticate(email=email, password=password)
    #         if not student:
    #             raise forms.ValidationError("User Does Not Exist.")
    #         if not student.check_password(password):
    #             raise forms.ValidationError("Password Does not Match.")
    #     return super(StudentLoginForm, self).clean(*args, **kwargs)

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name",
                  "last_name", 
                  "username", 
                  "email", 
                  "birth_date", 
                  "address",
                  "contact",
                  "roll",
                  "reg",
                  "department",
                  "year_of_study",
                  "photograph"
                  "password1",
                  "password2",
                   )

        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'birth_date':forms.DateField(widget=SelectDateWidget(years=range(1960, 2019), attrs={'class':'form-control'})),
            'address':forms.Textarea(attrs={'class':'form-control'}),
            'contact' : forms.TextInput(attrs={'class':'form-control'}),
            'roll' : forms.TextInput(attrs={'class':'form-control'}),
            'reg' : forms.TextInput(attrs={'class':'form-control'}),
            'department' : forms.TextInput(attrs={'class':'form-control'}),
            'year_of_study' : forms.TextInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.TextInput(attrs={'class':'form-control'}),
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birth_date = self.cleaned_data['birth_date']
        user.address = self.cleaned_data['address']
        user.contact = self.cleaned_data['contact']
        user.roll = self.cleaned_data['roll']
        user.reg = self.cleaned_data['reg']
        user.department = self.cleaned_data['department']
        user.year_of_study = self.cleaned_data['year_of_study']
        if commit:
            user.save()
        return user


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",   
            "address",
            "contact",
            "birth_date",
            "roll",
            "reg",
            "department",
            "year_of_study",
            "photograph"
        )

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'birth_date':forms.DateField(widget=SelectDateWidget(years=range(1995, 2002), attrs={'class':'form-control'})),
            'address':forms.Textarea(attrs={'class':'form-control'}),
            'contact' : forms.TextInput(attrs={'class':'form-control'}),
            'roll' : forms.TextInput(attrs={'class':'form-control'}),
            'reg' : forms.TextInput(attrs={'class':'form-control'}),
            'department' : forms.TextInput(attrs={'class':'form-control'}),
            'year_of_study' : forms.TextInput(attrs={'class':'form-control'}),
        }
        