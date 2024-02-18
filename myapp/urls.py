from django.urls import path
# from .views import MyModelList, MyModelDetail, FileUploadView
from . import views

urlpatterns = [
    
    path('uploadData/', views.handleDBUpload),

]