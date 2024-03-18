from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
   path('', views.index, name="index"),
   path('category/<int:category_pk>/', views.category_index, name="category_index"),
   path('create/', views.create, name='create'),
   path('<int:post_pk>/', views.detail, name='detail'),
   path('<int:post_pk>/update/', views.update, name='update'),
   path('<int:post_pk>/create/', views.comment_create, name="comment_create"),
   path('<int:post_pk>/update/<int:comment_pk>/', views.comment_update, name="comment_update"),
   path('<int:post_pk>/delete/<int:comment_pk>/', views.comment_delete, name="comment_delete"),
   path('<int:post_pk>/like/', views.like, name="like"),
   path('<int:post_pk>/like/<int:comment_pk>/', views.comment_like, name="comment_like"),
   # path('<int:post_pk>/reply/<int:comment_pk>/create/', views.reply_create, name="reply_create"),
   # path('<int:post_pk>/reply/<int:comment_pk>/detail/<int:reply_pk>/', views.reply_detail, name="reply_detail"),
]