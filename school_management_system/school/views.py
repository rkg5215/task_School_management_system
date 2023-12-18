from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, ClassForm, StudentUpdateForm, StudentStatusForm
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password, check_password


def checkusername(username): # Special Character not allowed
    if username != '' and all(chr.isalnum() or chr.isspace() for chr in username):
        return True
    else:
        return False

def uniqueemail(email):  # Email Should be unique
    search_email = User.objects.filter(email=email)
    if search_email:
        return False
    else:
        return True

def checkemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def checkpassword(password):  # Password format
    if password != '' :
        return True
    else:
        return False


def validate_registration(request,username,email,password):
    if checkusername(username)==False:
        messages.warning(request, "Username should contain only alphabets")
    elif checkemail(email)==False:
        messages.warning(request, "Enter a valid email address")
    elif uniqueemail(email)==False:
        messages.warning(request, "This Email is already Registered")
    elif checkpassword(password)==False:
        messages.warning(request, "Password can't be blank")
    else:
        return 1

def admin_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        psw = request.POST.get('password')
        repeat_psw= request.POST.get('psw_repeat')
        if validate_registration(request,username,email,psw) == 1:
            if psw == repeat_psw:
                password = make_password(psw)
                obj_user = User.objects.filter(username=username)
                if obj_user:
                    messages.warning(request, "Username already exists")
                    return render(request, "admin_register.html", locals())
                else:
                    newuser = User.objects.create(username=username, password = password, email=email)
                    newuser.save()
                    messages.success(request, "User Register Successfully.")
                    return redirect('admin_login')
            else:
                messages.warning(request, "Password and Confirm Password should be same")
        return render(request, "admin_register.html", locals())
    return render(request, "admin_register.html", locals())


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        psw = request.POST.get('password')
        try:
            get_user_by_username = User.objects.get(username=username)
            if get_user_by_username:
                flag = check_password(psw, get_user_by_username.password)
                if flag:
                    request.session["uid"] = request.POST.get('username')
                    messages.success(request, "Login Successfully.")
                    return redirect('dashboard')
                messages.warning(request, "Wrong password")
                return render(request, "admin_login.html", locals())
        except:
            messages.error(request, "Wrong username or password")
            return render(request, "admin_login.html", locals())
    return render(request, "admin_login.html", locals())


def dashboard(request):
    if request.session.has_key('uid'):
        user_name = (request.session["uid"]).capitalize()
        total_class = Class.objects.count()
        total_students = Student.objects.count()
        active_students = (Student.objects.filter(status="active")).count()
        inactive_students = (Student.objects.filter(status="inactive")).count()
        return render(request, 'dashboard.html',locals())
    if request.session.has_key('student'):
        user_name = (request.session["student"]).capitalize()
        messages.warning(request, "You Don't Have Permission for this")
        return render(request, 'student_dashboard.html', locals())
    else:
        return redirect('admin_login')


def students(request):
    if request.session.has_key('uid'):
        user_name = (request.session["uid"]).capitalize()
        students_list = Student.objects.all()
        form = StudentRegistrationForm()
        return render(request, 'students.html', locals())
    else:
        return redirect('admin_login')

def register_student(request):
    if request.session.has_key('uid'):
        if request.method == 'POST':
            form = StudentRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Student Register Successfully")
                return redirect('students')
            messages.error(request,"Invalid Format")
            return redirect('students')
    else:
        return redirect('admin_login')


def student_status(request,id):
    if request.session.has_key('uid'):
        instance = Student.objects.get(id=id)
        form = StudentStatusForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Student Status Change Successfully")
            return redirect('students')
        messages.warning(request, "Please Select Correct Value")
        return redirect('students')
    else:
        return redirect('admin_login')


def all_class(request):
    if request.session.has_key('uid'):
        user_name = (request.session["uid"]).capitalize()
        form = ClassForm()
        class_list = Class.objects.all()
        return render(request, 'all_class.html', locals())
    else:
        return redirect('admin_login')


def add_class(request):
    if request.session.has_key('uid'):
        if request.method == 'POST':
            form = ClassForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Class Added Successfully")
                return redirect('class')
            else:
                messages.error(request, "Invalid Format")
                return redirect('all_class')
    else:
        return redirect('admin_login')


def admin_logout(request):
    try:
        del request.session["uid"]
    except KeyError:
        pass
    return redirect("/admin_login")

def logout(request):
    try:
        del request.session["student"]
        del request.session["phone"]
    except KeyError:
        pass
    return redirect("/student_login")


def student_login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        try:
            student = Student.objects.get(phone=phone, password=password)
            name = student.first_name
            phone = student.phone
            if student and student.status=="active":
                request.session["student"] = name
                request.session["phone"] = phone
                messages.success(request, "Login Successfully.")
                return redirect('student_dashboard')
            messages.warning(request,"Only Active Student Can Login!")
            return render(request, 'student_login.html')
        except:
            messages.warning(request, "Please Check your Credentials!")
            return render(request, 'student_login.html')
    return render(request, 'student_login.html')

def student_dashboard(request):
    if request.session.has_key('student'):
        user_name = (request.session["student"]).capitalize()
        phone= request.session["phone"]
        students_list = Student.objects.filter(phone=phone)
        form = StudentRegistrationForm()
        return render(request, 'student_dashboard.html', locals())
    else:
        return redirect('student_login')

def profile(request):
    if request.session.has_key('student'):
        user_name = (request.session["student"]).capitalize()
        if request.method == 'POST':
            phone = request.session["phone"]
            instance = Student.objects.get(phone=phone)
            form = StudentUpdateForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile Update Successfully")
                return redirect('profile')
            messages.warning(request, "Wrong Entry")
            return redirect('profile')
        else:
            phone = request.session["phone"]
            instance = Student.objects.get(phone=phone)
            form = StudentUpdateForm(instance=instance)
            image_path=instance.image
            return render(request, 'profile.html', {'form': form, 'user_name': user_name, 'image_path':  image_path})
    else:
        return redirect('student_login')