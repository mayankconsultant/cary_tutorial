from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

# Create your views here.

# posts =[
#     {
#         'author':'Mayank',
#         'title':'Arrange Marriage Vs Love Marriage',
#         'content':"It doesn't matter",
#         'date_posted':"20-Aug-2020"
#     },
#     {
#         'author': 'Foram',
#         'title': 'Famous Personality Vs Rich Personality',
#         'content': "It doesn't matter",
#         'date_posted': "21-Aug-2020",
#     }
# ]

from .models import Post
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView
                                  )


@login_required
def home(request):
    context = {'posts': Post.objects.all()
               }
    return render(request, 'blog/home.html', context)


# template will be searched as <app>/<model>_<viewtype>.html
# @login_required
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        # form.instance.title = 'New Title Expected'
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView (LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# template will be searched as <app>/<model>_<viewtype>.html
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def about(request):
    context = {'title': 'About'}
    return render(request, 'blog/about.html', context)
