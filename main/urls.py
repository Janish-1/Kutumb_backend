from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserList.as_view()),                 
    path('users/<int:pk>/', UserDetail.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path('otp-verify/', otpverify.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('update-password/', PasswordUpdateView.as_view()),
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('allpost/', PostListAPIViews.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('comments/<int:post_id>/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('like/<int:post_id>/', LikePostAPIView.as_view(), name='like_post'),
    path('unlike/<int:post_id>/', UnLikePostAPIView.as_view(), name='like_post'),
    path('gallery/', GalleryListAPIView.as_view(), name='gallery-list'),
    path('request_table/', RequestTableAPIView.as_view(), name='request-table'),
    path('action/', ActionListAPIView.as_view(), name='action-list'),
    path('donations/', ActionListDonationAPIView.as_view(), name='action-list'),
    path('celebrations/', ActionListCelebrationAPIView.as_view(), name='action-list'),
    path('sub/', SubscriptionPaymentView.as_view(), name='transactions'),
]
