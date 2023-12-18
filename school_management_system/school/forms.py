from django import forms
from .models import Student
from .models import Class

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'date_of_birth','status', 'image', 'student_class']
        widgets = {
                    'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                    'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                    'phone': forms.TextInput(attrs={'class': 'form-control'}),
                    'email': forms.EmailInput(attrs={'class': 'form-control'}),
                    'password': forms.PasswordInput(attrs={'class': 'form-control'}),
                    'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)','class': 'form-control'}),
                    'image': forms.FileInput(attrs={'class': 'form-control'}),
                    'status': forms.Select(attrs={'class': 'form-control'}),
                    'student_class': forms.Select(attrs={'class': 'form-control'}),
                    }

class StudentStatusForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['status']


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'date_of_birth', 'image', 'student_class']
        widgets = {
                    'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                    'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                    'phone': forms.TextInput(attrs={'class': 'form-control'}),
                    'email': forms.EmailInput(attrs={'class': 'form-control'}),
                    'password': forms.PasswordInput(render_value= True,attrs={'class': 'form-control'}),
                    'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
                    'image': forms.FileInput(attrs={'class': 'form-control'}),
                    'student_class': forms.Select(attrs={'class': 'form-control'}),
                   }




class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name', 'class_details']
        widgets = {
                    'class_name' : forms.TextInput(attrs={'class':'form-control'}),
                    'class_details': forms.TextInput(attrs={'class': 'form-control'}),

                   }