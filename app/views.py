from django.shortcuts import render, redirect
from .forms import UserProfileForm, BlogPostForm
from .models import UserProfile, BlogPost
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages

# Create your views here.
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def index(request):

    return render(request, 'index.html')

def register_user(request):
    if request.session.get('user_id') and request.session.get('user_type'):
        return redirect('dashboard')

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login') 
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserProfileForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.session.get('user_id') and request.session.get('user_type'):
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = UserProfile.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_type'] = user.user_type
                return redirect('dashboard') 
            else:
                error_message = "Invalid credentials. Please try again."
        except UserProfile.DoesNotExist:
            error_message = "User does not exist. Please register first."
        return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def logout_user(request):
    request.session.flush() 
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

@login_required
def dashboard(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    user = UserProfile.objects.get(id=user_id)

    if user_type == 'doctor':
        return render(request, 'doctor_dashboard.html', {'user':user})
    elif user_type == 'patient':
        return render(request, 'patient_dashboard.html', {'user':user})
    else:
        return redirect('login')

@login_required
def create_blog(request):
    if request.session.get('user_type') != 'doctor':
        return redirect('dashboard')  
    
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            user = UserProfile.objects.get(id=request.session.get('user_id'))
            blog.author = user
            blog.save()
            return redirect('dashboard') 
    else:
        form = BlogPostForm()

    return render(request, 'create_blog.html', {'form': form})

@login_required
def all_blogs(request):
    blog_posts = BlogPost.objects.filter(is_draft=False).order_by('category')
    categories = ['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']  
    categorized_posts = {category: [] for category in categories}

    for post in blog_posts:
        categorized_posts[post.category].append(post)
        
    return render(request, 'all_blogs.html', {'categorized_posts': categorized_posts})

@login_required
def my_blogs(request):
    if request.session.get('user_type') != 'doctor':
        return redirect('dashboard') 

    user_id = request.session.get('user_id')
    published_blogs = BlogPost.objects.filter(author=user_id, is_draft=False)
    draft_blogs = BlogPost.objects.filter(author=user_id, is_draft=True)

    return render(request, 'my_blogs.html', {'published_blogs': published_blogs,
        'draft_blogs': draft_blogs})