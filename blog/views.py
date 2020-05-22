from django.shortcuts import render,HttpResponse ,redirect
from blog.models import Post , BlogComment
from django.contrib import messages


# Create your views here.




def blogHome(request):
    allPosts = Post.objects.all()
    context ={'allPosts':allPosts}
    # print(allPosts)
    return render(request, 'blog/blogHome.html',context)
    # return HttpResponse("This is blog Home we will keep  all post here..") 

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    comments =BlogComment.objects.filter(post=post)
    context = {'post':post,'comments':comments,'user':request.user}
    return render(request,'blog/blogPost.html',context)
    # return HttpResponse(f'This is blog:{slug}')     


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno") 
        post = Post.objects.get(sno=postSno) 
        comment = BlogComment(comment=comment,user=user,post=post)
        comment.save()
        messages.success(request,"Your post has been posted Successfully")
        


    return redirect(f"/blog/{post.slug}")
    
    