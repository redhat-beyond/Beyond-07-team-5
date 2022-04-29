from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)
from .models import Post, Resume


class PostListView(ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  # order posts from newest to oldest

    def get_context_data(self, **kwargs):
        ctx = super(PostListView, self).get_context_data(**kwargs)
        ctx['title'] = 'feed'
        return ctx


class PostDetailView(DetailView):
    model = Post
    # Django's default template name - posts/post_detail.html
    context_object_name = 'post'


class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    # Django's default template name - posts/post_form.html
    fields = ['description', 'resume_file']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(ResumeCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'resume-create'
        return ctx


def about(request):
    return render(request, 'posts/about.html', {'title': 'about'})


def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        objlst = Post.objects.all()
        posts = objlst.filter(description__icontains=searched)
        return render(request, 'posts/search.html', {'posts': posts, 'searched':searched})

    return render(request, 'posts/search.html', {})
