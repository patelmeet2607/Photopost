from django.urls import include,path
from rest_framework import routers
from .views import UserLogin,RegisterView,UploadView,GetAllImagesView,LikeView,GetUserImagesView

urlpatterns = [
    path('login',UserLogin.as_view(), name='login'),
    path('register',RegisterView.as_view(), name='register'),
    path('image_upload',UploadView.as_view(), name='image_upload'),
    path('get_user_img',GetUserImagesView.as_view(), name='get_user_img'),
    path('get_all_img',GetAllImagesView.as_view(), name='get_all_img'),
    path('like',LikeView.as_view(), name='like'),
]