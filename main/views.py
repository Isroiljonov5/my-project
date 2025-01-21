from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post
from django.db.models import Max

# Create your views here.

def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page")
    page_objects = paginator.get_page(page_number)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if all([title,content]):
            Post.objects.create(title=title, content=content)
            messages.success(request,"Post Created !")
        
    return render(request, "pages/home.html", context={"page_objects":page_objects,})




def add_votes(request, post_id):
    post = Post.objects.get(id=post_id)
    
    request.session.modified = True
    try:
        voted_posts = request.session["vote_list"]
    except: 
        voted_posts = request.session["vote_list"] = []
    # print(request.session.get("voted_posts"))
    if post.id in voted_posts:
        voted_posts.remove(post.id)
        post.votes -= 1
        post.save()
        messages.info(request, "Vote removed !")
    else:
        voted_posts.append(post.id)
        post.votes += 1
        post.save()
        messages.info(request, "Vote added !")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))





def filter_vote(request, filter_by_what):
    if filter_by_what.lower() == "by_votes":
        posts = Post.objects.annotate(Max("votes")).order_by("-votes__max")
        paginator = Paginator(posts, 2)
        page_number = request.GET.get("page")
        page_objects = paginator.get_page(page_number)
        return render(request, "pages/home.html", context={"page_objects":page_objects,})
    elif filter_by_what.lower() == "recent":
        posts = Post.objects.all().order_by("-created_at")
        paginator = Paginator(posts, 2)
        page_number = request.GET.get("page")
        page_objects = paginator.get_page(page_number)
        return render(request, "pages/home.html", context={"page_objects":page_objects,})
    else:
        return redirect("/")


# def home(request):
#     return render(request, 'pages/home.html')