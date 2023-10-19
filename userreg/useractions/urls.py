
from django.urls import path, include
from .views import *

urlpatterns = [
    path('reg', UserActions.as_view(), name='reg'),
    path('login', userLogin.as_view(), name='login'),
    path('logout', userLogout.as_view(), name='logout'),
    path('adminurls', adminPanel.as_view(), name='adminurls'),
]