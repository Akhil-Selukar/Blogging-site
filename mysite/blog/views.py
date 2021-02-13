from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,
                                    DeleteView)

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    #if not logged in redirect back to login page
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    #if not logged in redirect back to login page
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PoseDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    # if deletion is success it will redirect to post_list which will call PostListView (check views.py).
    #post_lazy will wait till it get the success message
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    #if not logged in redirect back to login page
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    #if it is the list of drafts then its publish date must be published_date__isnull
    #thats what we are checking with below queryset
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

######################################
########### Comment Views ############
######################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post = post  #assigning that perticular comment to perticular post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})


@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk  #after deletion of the comment we will never be able to get
                               # post.pk i.e. promary key of the associated post
                               # hence we stored it in the veriable first and then deleted the comment.
    comment.delete()
    return redirect('post_detail',pk=post_pk)
