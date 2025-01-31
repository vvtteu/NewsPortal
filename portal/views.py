from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import *
from .filters import PostFilter
from .forms import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_created'] = datetime.utcnow()
        context['all_posts'] = self.get_queryset().count()
        return context


class PostDetail(LoginRequiredMixin, DetailView): 
    model = Post
    template_name = 'new.html' 
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_created'] = datetime.utcnow()
        return context


class SearchPosts(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView): 
    permission_required = ('portal.add_post',
                           'portal.change_post',
                           'portal.delete_post'
                           )
    model = Post
    template_name = 'news_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        return super().form_valid(form)
    

class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  
    permission_required = ('portal.add_post',
                           'portal.change_post',
                           'portal.delete_post'
                           )
    
    model = Post
    template_name = 'article_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('portal.add_post',
                           'portal.change_post',
                           'portal.delete_post'
                           )
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('portal.add_post',
                           'portal.change_post',
                           'portal.delete_post'
                           )
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')


class NewsUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('portal.add_post',
                           'portal.change_post',
                           'portal.delete_post'
                           )
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('portal.add_post',
                           'portal.change_post',
                           'portal.delete_post'
                           )
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')



#для лк и стать автором

def personal_account_view(request):
    is_not_author = not request.user.groups.filter(name='authors').exists()
    return render(request, 'account/lk.html', {
        'username': request.user.username,
        'is_not_author': is_not_author
    })


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('lk')
