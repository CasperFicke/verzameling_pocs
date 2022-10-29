# theblog/urls.py

# Django
from django.urls import path, include

#from rest_framework import routers

#from . import views

# import views
from .views import BlogsView, BlogPostView, AddBlogPostView, EditBlogPostView, DeleteBlogPostView, LikeView, AddCommentView, EditCommentView, DeleteCommentView, TagsView, AddTagView, Search_results

urlpatterns = [
  # blogposts  
  path ('blogposts/'               , BlogsView.as_view(), name='all-blogposts'),
  path ('blogposts/search/'        , Search_results, name='search-blogposts'),
  path ('blogposts/<int:pk>'       , BlogPostView.as_view(), name='show-blogpost'),
  path ('blogposts/add/'           , AddBlogPostView.as_view(), name='add-blogpost'),
  path('blogposts/<int:pk>/edit/'  , EditBlogPostView.as_view(), name='edit-blogpost'),
  path('blogposts/<int:pk>/delete/', DeleteBlogPostView.as_view(), name='delete-blogpost'),

  # tags
  path ('tags/'        , TagsView.as_view(), name='all-tags'),
  path ('tags/add/'    , AddTagView.as_view(), name='add-tag'),
  
  # likes
  path('like/<int:pk>' , LikeView, name='like-post'), # like a post
  # comments
  #path ('blogposts/<int:pk>/comments/' , CommentsView.as_view(), name='show-comments'),
  path('blogposts/<int:pk>/comments/add/', AddCommentView.as_view(), name='add-comment'),
  path('blogposts/<int:blogpost_id>/comments/<int:pk>/edit/'  , EditCommentView.as_view(), name='edit-comment'),
  path('blogposts/<int:blogpost_id>/comments/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete-comment'),
]
