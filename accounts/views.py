from django.shortcuts import render, HttpResponse, redirect
from .forms import userRegistrationForm
from .models import User, UserProfile
from .utils import detectUser
from vendor.forms import vendorRegistrationForm

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied



#RESTRICT THE VENDOR FROM ACCESSING THE CUSTOMER PAGE.
def check_role_vender(user):
    if user == 1:
        return True
    else:
        raise PermissionDenied

#RESTRICT THE CUSTOMER FROM ACCESSING THE VENDOR PAGE.
def check_role_customer(user):
    if user == 2:
        return True
    else:
        raise PermissionDenied


# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.error(request,'You are already logged in!')
        return redirect('custDashboard')
    elif request.method == 'POST':
        print(request.POST) #request.POST, WE ARE GETTING THE DATA HERE.
        form = userRegistrationForm(request.POST)
        if form.is_valid():

            # CREATE THE USER, USING THE FORM

            # password = form.cleaned_data['password']
            # user = form.save(commit=False) #FORM IS READY TO BE SAVED, BUT NOT YET SAVED. BCZ OF COMMIT
            # user.role = User.CUSTOMER
            # user.set_password(password)
            # user.save()

            # CREATE THE USER, USING create_user METHOD.
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            #print("User is created")

            messages.success(request, "Your account has been registered successfully!")
            return redirect('registerUser')
        else:
            print("Invalid form")
            print(form.errors)
    else:
        form = userRegistrationForm()
    
    
    context = {
        'form':form
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.error(request,'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        #store the data and create a user
        form = userRegistrationForm(request.POST)
        v_form = vendorRegistrationForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "You account has been registered successfully! Please wait for admin approval.")
        else:
            print("Invalid Form")
            print(form.errors)
    else: 
        form = userRegistrationForm()
        v_form = vendorRegistrationForm()
    context = {
        'form':form,
        'v_form':v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.error(request,'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('myAccount') 
        else:
            messages.error(request, 'Invalid Login Credentials.')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out!')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vender)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')
