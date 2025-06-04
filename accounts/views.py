from django.shortcuts import render, HttpResponse
from .forms import userRegistrationForm

# Create your views here.
def registerUser(request):
    form = userRegistrationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/registerUser.html', context)
