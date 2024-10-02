from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    return render(request,'blogapp/index.html')

# register user

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    context = {'form':form}
    return render(request,'blogapp/register.html',context=context)

# login a user

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('dashboard')
   
    context = {'form2': form}
    return render(request,'blogapp/my-login.html',context=context)


# dasboard 
@login_required(login_url='login')
def dashboard(request):
    posts = Post.objects.all().order_by('-created_at') 
    paginator = Paginator(posts, 2) 

    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 

    context = {
        'page_obj': page_obj,
    }
    return render(request,'blogapp/dashboard.html',context=context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('dashboard')

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('dashboard')  # Redirect to the post list or the specific post
    else:
        form = CommentForm()
    return render(request, 'blogapp/comment-post.html', {'form': form, 'post': post})

# post a blog 

def post_blog(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            return redirect('dashboard') 
    else:
        form = PostForm()
    
    return render(request, 'blogapp/create-post.html', {'form': form})


# user logout

def user_logout(request):
    auth.logout(request)
    return redirect('login')
