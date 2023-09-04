from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    #check to see if logged in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
    #authenticate
        user = authenticate(request,username=username, password=password)   
        if user is not None:
            login(request,user)
            messages.success(request,"You have been successfully logged in!!") 
            return redirect('home')
        else:
            messages.success(request,"Username and password dont match")
            return redirect('home')
    else:    
      return render(request, 'home.html',{'records':records})
    
def logout_user(request):
    logout(request)
    messages.success(request,"You have logged out successfully!!")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
          form = SignUpForm(request.POST)
          if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,'You are successfully registered!!!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})   
    return render(request,'register.html',{'form':form})     


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
      if request.method == "POST":
          if form.is_valid():
              add_record = form.save()
              messages.success(request,"Record added successfully...")
              return redirect('home')
      return render(request,'add_record.html',{'form':form})  

    else:
        messages.success(request,"You must be logged in...")
        return redirect('home')     


def record_customer(request,pk):
    if request.user.is_authenticated:
         record_customer = Record.objects.get(id=pk)
         return render(request,'record.html',{'record_customer':record_customer})
    
    else:
       messages.success(request,'You musted logged in..')
       return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_record = Record.objects.get(id=pk)
        delete_record.delete()
        messages.success(request,"Information successfully deleted..")
        return redirect('home')
    else:
        messages.success(request,"You musted be logged in..")
        return render(request,'record.html')   

def update_record(request,pk):
     if request.user.is_authenticated:
         current_record = Record.objects.get(id=pk)
         form = AddRecordForm(request.POST or None,instance=current_record)
         if form.is_valid():
             form.save()
             messages.success(request,"Updated Successfully...")
             return redirect('home')
         return render(request,'update_record.html',{'form':form}) 
     else:
        messages.success(request,"you musted be logged in...")
        return redirect('home')    







