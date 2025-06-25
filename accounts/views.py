from django.shortcuts import render, HttpResponse, redirect
from .forms import userRegistrationForm
from .models import User, UserProfile
from .utils import detectUser, send_verification_email
from vendor.forms import vendorRegistrationForm

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



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
            
            #AFTER THE USER IS SAVED, WE WILL SEND THE VERIFICATION EMAIL.
            mail_subject = 'Activate your account.'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

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

def activate(request, uidb64, token):

    #ACTIVATE THE USER BY SETTING THE is_active STATUS TO TRUE.
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')

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

            #SEND VERIFICATION EMAIL
            mail_subject = 'Activate your account.'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

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

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email'] #GETTING THE EMAIL.

        if User.objects.filter(email=email).exists(): #CHECKING THE EMAIL IN THE DATABASE.
            user = User.objects.get(email__exact=email)

            #SEND PASSWORD RESET EMAIL.
            mail_subject = 'Reset your password.'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exists.')
            return redirect('forgot_password')


    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')

 
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')
