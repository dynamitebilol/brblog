import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,  DeleteView
from django.core.paginator import Paginator
from hitcount.views import HitCountDetailView
from requests import request
from .models import Comment, Post
from .forms import CommentForm, PostForm


# def all_posts(request):
#     posts = Post.objects.all().order_by('created_on')
#     p = Paginator(posts, 5)
#     page_number = request.GET.get('page')
#     page_obj = p.get_page(page_number)  # returns the desired page object
  
#     context = {'page_obj': page_obj, 
#                "posts":posts,
#                 }
#     return render(request, 'all_posts.html', context)

class AllPostView(ListView):
    paginate_by = 6
    model = Post
    template_name = 'all_posts.html'
    context_object_name = 'posts'

@login_required(login_url='post:login')
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })
        

        



class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'
    context_object_name = 'results'
    

    def get_queryset(self): # new
        query = self.request.GET.get('title')
        results =  Post.objects.filter(title__icontains=query)
        return results



class PostListView(ListView):
    model = Post
    template_name = "index.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs_json"] = json.dumps(list(Post.objects.values('title')))
        context['older_posts'] =  Post.objects.all().order_by('created_on')[:4]
        context['posts'] = Post.objects.all().order_by('-created_on')
        context['popular_posts'] = Post.objects.all().order_by('-hit_count_generic__hits')[:6]
        return context



def update_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Post, slug=slug)
 
    if request.user == obj.author:
        # pass the object as instance in form
        form = PostForm(request.POST, request.FILES, instance = obj)
    
        # save the data from the form and
        # redirect to detail_view
        if form.is_valid():
            form.save()
            return redirect("/"+slug)
    
        # add form dictionary to context
        context["form"] = form
        context["obj"] = obj
        

        return render(request, "post_update.html", context)

    else:
        messages.info(request, "You can only change your own post! ")
        return redirect('/')



class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    context_object_name = 'obj'
    success_url = "/"




# def post_list(request):
#     posts = Post.objects.all().order_by('-created_on')
#     older_posts = Post.objects.all().order_by('created_on')
#     context = {
#         'posts': posts,
#         'older_posts':older_posts
#     }
#     return render(request, 'index.html', context)

        
    

@login_required(login_url='post:login')
def create(request):
    if request.method == "POST":
        author = request.user
        title = request.POST['title']
        image = request.FILES.get('image')
        content = request.POST['content']

        new_post = Post.objects.create(author=author, title=title, image=image, content=content)
        new_post.save()
        return redirect('/')
    else:
        return render(request, 'post_form.html')


class PostDetailView(HitCountDetailView):
    model = Post
    template_name ='post_detail.html'
    context_object_name = 'post'
    count_hit = True


    def get_context_data(self, **kwargs):

        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(
            blogpost_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        data['popular_posts'] =  Post.objects.order_by('-hit_count_generic__hits')[:6]
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        return data


    def post(self, request, *args, **kwargs):

            new_comment = Comment(content=request.POST['content'],
                                        author=self.request.user,
                                        blogpost_connected=self.get_object())
            new_comment.save()
            return self.get(self, request, *args, **kwargs)

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email is taken")
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username is taken")
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

        else:
            messages.info(request, "Passwords Not Matching")
            return redirect('/')

    elif request.user.is_authenticated:
        return redirect('/')
                
    else:
        return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Credentials is invalid")

    elif request.user.is_authenticated:
        return redirect('/')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def page_not_found_view(request, exception):
    return render(request, 'error_404.html', status=404)