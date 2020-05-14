from django.shortcuts import render,HttpResponse
from home.models import Contact
from django.contrib import messages
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