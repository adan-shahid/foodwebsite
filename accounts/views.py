from django.shortcuts import render, HttpResponse, redirect
from .forms import userRegistrationForm
from .models import User

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        print(request.POST) #request.POST, WE ARE GETTING THE DATA HERE.
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()
            return redirect('registerUser')
    else:
        form = userRegistrationForm()
    
    form = userRegistrationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/registerUser.html', context)
