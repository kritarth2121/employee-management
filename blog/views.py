from django.shortcuts import render, get_object_or_404
from django import forms

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from users import views as user_views

from .models import Post
from django.db.models.functions import datetime
from django.contrib.admin import widgets                                       
from django.contrib.auth.decorators import user_passes_test
def home(request):
    if request.user.is_superuser:
        
        context = {
            'posts': Post.objects.all()
        }
        print(context)
        return render(request, 'blog/home.html', context)
    if request.user.is_authenticated:
        user=request.user.id
        context = {
            'posts': Post.objects.filter(assigned_employee=user)
        }
        return render(request, 'blog/home.html', context)
    else:

        return render(request, 'login')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        print(self.request.user)
        print(Post.objects.all())
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        return Post.objects.filter(assigned_employee__username=user).order_by('-date_posted')
        
class Work(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        
        return Post.objects.filter(assigned_employee__username=self.request.user).order_by('-date_posted')
        
class PostDetailView(ListView):
    model = Post
    
    template_name = 'blog/post_detail.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    def get_queryset(self):
        user = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        print(user.id)
        return Post.objects.filter(id=user.id)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['assigned_employee','work', 'description','status','deadline']
    
    def form_valid(self, form):
            return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False
        


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['assigned_employee','work', 'description','status','deadline']
    
    def form_valid(self, form):
        form.instance.assigned_employee = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False
    #print(post.id)

     
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        
        if self.request.user.is_superuser:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
