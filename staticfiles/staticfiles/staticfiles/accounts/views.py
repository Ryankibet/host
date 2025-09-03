from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden

#Register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            try:
               user = User.objects.create_user(username=username,password=password)
               user.save()
               print(user)
               messages.success(request, "Account created successfully ")
               return redirect('login_view') 
            except:
               messages.error(request, "")
    else:
     messages.error(request, "")
     
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == "POST":
       username = request.POST['username']
       password = request.POST['password']

       user = authenticate(request, username=username, password=password)

       if user is not None:
          login(request, user)
          messages.success(request, "You are successfully logged in")
          return redirect("myapp:index")
       else:
          messages.error(request, "Invalid login credentials")

       

    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')  # Redirect to login page
    else:
        return HttpResponseForbidden("Forbidden: This URL only accepts POST requests.")