from django.shortcuts import render,HttpResponse , redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Post
#from datetime import datetime

# Create your views here.


def home(request):
    allPosts = Post.objects.all()
    context ={'allPosts':allPosts}
    return render(request,'home/home.html',context)
    # return HttpResponse("This is home page")

def contact(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        # print(name,email,phone,content)
        # This condition is writted for alert messages after submiting the contact form
        
        if len(name)<2 or len(email)<2 or len(phone)<10 or len(content)<3:
            messages.error(request,"Please fill the Detail correctly!")
        else:    
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Your Detail has been submitted successfully ")


    return render(request,'home/contact.html')


def about(request):
    return render(request,'home/about.html')



def search(request):
    query = request.GET['query']
    if len(query)>70:
        allPosts = Post.objects.none()
    else:
    # allPosts = Post.objects.all()
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,"No Results found. Please refine your query!")
    params = {'allPosts':allPosts,'query':query}
    # return HttpResponse("this is search page")
    return render(request,'home/search.html',params)

def handleSignup(request):
    # Get the post parameters
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # check for errorneous inputs
        if len(username) > 10:
            messages.error(request,"User mube be under 10 character")
            return redirect("home")
        
        # user should be alphanumeric
        if not username.isalnum():
            messages.error(request,"User should only contain letter and number ") 
            return redirect("home")
       
        # password should match
        if pass1 != pass2:  
            messages.error(request,"Password do not match ")
            return redirect("home")     

        # create the user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your account has been successfully created.")
        return redirect("home")
    else:
        return HttpResponse("404 - Not found ")  

def handleLogin(request):
     # Get the post parameters
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect("home") 
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect("home")           
    return HttpResponse("404 - Not found ")  
    

def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully Logout ")
    return redirect("home")        


