from django.urls import path
from .views import logout_view, login_view
from .forms import LoginForm

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # Outras URLs do aplicativo auth_app...
]
