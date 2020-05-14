from django.shortcuts import render,HttpResponse
from blog.models import Post

# Create your views here.




def blogHome(request):
    allPosts = Post.objects.all()
    context ={'allPosts':allPosts}
    # print(allPosts)
    return render(request, 'blog/blogHome.html',context)
    # return HttpResponse("This is blog Home we will keep  all post here..") 

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    print(post)
    context = {'post':post}
    return render(request,'blog/blogPost.html',context)
    # return HttpResponse(f'This is blog:{slug}')     