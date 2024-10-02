from django.urls import path
from . import views



urlpatterns = [
    path('register',views.register,name='register'),
    path('my-login', views.my_login,name='login'),
    path('logout', views.user_logout,name='logout'),
    path('', views.dashboard,name='dashboard'),
    path('post/', views.post_blog, name='post-blog'),
    path('post/<int:post_id>/like/', views.like_post, name='like-post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment-post'),
]
