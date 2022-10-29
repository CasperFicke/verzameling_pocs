# theblog/views.py
# function - en classbased views

# django
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

# local
from .models import BlogPost, Tag, Comment
from .forms import PostForm, EditBlogpostForm, TagForm, CommentForm

# tbv rest API's
#from rest_framework import viewsets
#from .serializers import BlogPostSerializer

# All blogposts
class BlogsView(ListView):
  model               = BlogPost
  context_object_name = 'blogposts'
  template_name       = 'theblog/all_blogposts.html'
  ordering            = ['-post_date']

  # function to make data usable in html
  def get_context_data(self, *args, **kwargs):
    title = 'Blogposts'
    context  = super(BlogsView, self).get_context_data(*args, **kwargs)
    context['title'] = title
    return context

# Show blogpost
class BlogPostView(DetailView):
  model         = BlogPost
  template_name = 'theblog/show_blogpost.html'

  # function to make data usable in html
  def get_context_data(self, *args, **kwargs):
    context  = super(BlogPostView, self).get_context_data(*args, **kwargs)
    # total likes
    stuff       = get_object_or_404(BlogPost, id=self.kwargs['pk'])
    total_likes = stuff.total_likes()
    
    # liked status
    liked=False
    if stuff.likes.filter(id=self.request.user.id).exists():
      liked = True
    
    #context["cat_menu"] = cat_menu
    context["total_likes"] = total_likes
    context["liked"] = liked
    return context

# like blogpost
def LikeView(request, pk):
  blogpost = get_object_or_404(BlogPost, id=request.POST.get('blogpost_id'))
  liked = False
  if blogpost.likes.filter(id=request.user.id).exists():
    blogpost.likes.remove(request.user)
    liked = False
  else:
    blogpost.likes.add(request.user)
    liked = True
  return HttpResponseRedirect(reverse('show-blogpost', args=[str(pk)]))
    
# add blogpost
class AddBlogPostView(LoginRequiredMixin, CreateView):
  model         = BlogPost
  form_class    = PostForm
  template_name = 'theblog/add_blogpost.html'
  # fields      = '__all__'
  # function to get userid of loggendin user and use it to assign the new blogpost to this user
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

# edit blogpost
class EditBlogPostView(UpdateView):
  model         = BlogPost
  form_class    = EditBlogpostForm
  template_name = 'theblog/edit_blogpost.html'
  # fields      = ['title', 'title_tag', 'body'] (geen field in geval van gebruik form)

# delete post
class DeleteBlogPostView(DeleteView):
  model         = BlogPost
  template_name = 'theblog/delete_blogpost.html'
  success_url   = reverse_lazy('all-blogposts')

# Search blogpost
def Search_results(request):
  response = None
  blogpost = request.POST.get('blogpost')
  qs = BlogPost.objects.filter(title__icontains=blogpost)
  if len(qs) > 0 and len(blogpost) > 0:
    data=[]
    for bpost in qs:
      item = {
        'pk'     : bpost.pk,
        'title'  : bpost.title,
        'snippet': bpost.snippet,
        'image'  : str(bpost.header_image.url)
      }
      data.append(item)
    response = data
  else:
    res = 'Geen blogpost(s) gevonden'
  return JsonResponse({'data': response})


# Blog view
#class BlogView(viewsets.ModelViewSet):
#  queryset         = BlogPost.objects.all()
#  serializer_class = BlogPostSerializer

# All tags
class TagsView(ListView):
  model               = Tag
  context_object_name = 'tags'
  template_name       = 'theblog/all_tags.html'
  ordering            = ['caption']

  # function to make data usable in html
  def get_context_data(self, *args, **kwargs):
    title = 'tags'
    context  = super(TagsView, self).get_context_data(*args, **kwargs)
    context['title'] = title
    return context

# add tag
class AddTagView(LoginRequiredMixin, CreateView):
  model         = Tag
  form_class    = TagForm
  template_name = 'theblog/add_tag.html'
  success_url   = reverse_lazy('all-tags')
  #fields      = '__all__'
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

# add comment
#@login_required
class AddCommentView(LoginRequiredMixin, CreateView):
  model         = Comment
  form_class    = CommentForm
  template_name = 'theblog/add_comment.html'
  # redirect to blogpost
  def get_success_url(self):
     return reverse_lazy('show-blogpost', kwargs={'pk': self.kwargs['pk']})
  # function to get userid of loggendin user and use it to assign new comment to the l;oggedin user
  def form_valid(self, form):
    form.instance.blogpost_id = self.kwargs['pk']
    form.instance.author      = self.request.user
    return super().form_valid(form)

# edit comment
class EditCommentView(UpdateView):
  model         = Comment
  form_class    = CommentForm
  template_name = 'theblog/edit_comment.html'
  success_url   = reverse_lazy('all-blogposts')
  # moet eigenlijk naar blogpost waar dit comment bij hoort
  
# delete comment
class DeleteCommentView(DeleteView):
  model         = Comment
  template_name = 'theblog/delete_comment.html'
  success_url   = reverse_lazy('all-blogposts')
