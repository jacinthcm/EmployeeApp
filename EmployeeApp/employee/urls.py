from django.urls import path, include
from employee.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('employee', EmployeeViewSet)

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('', include(router.urls)),

]
