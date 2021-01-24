from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.UserLoginView.as_view(), name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('edit/', authapp.edit, name='edit'),
    path('register/', authapp.UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', authapp.UserProfileView.as_view(), name='profile'),
    # path('profile/', authapp.profile, name='profile'),
    path('verify/<email>/<activation_key>', authapp.verify, name='verify')
]
