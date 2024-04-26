from django.urls import path
from .views import SignUpAPIView, UserListAPIView, UserLoginView, UpdateExcelAPIView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('xlxs_upload/', UpdateExcelAPIView.as_view(), name='xls-sheet'),
]
