from django.urls import path 
from . import views 

urlpatterns = [
    #Get all jobs without children elements like Panels
    path('api/jobs', views.JobList.as_view(), name='job_list'),
    #Get for a Job all Child elements and detals
    path('api/job_detail/<int:pk>', views.JobDetail.as_view(), name='job_detail'),
    #Get a image from the django server
    path('data/panel_images/<str:image_path>', views.panel_image),
    path('data/cropped_panel_images/<str:image_path>', views.cropped_panel_image),
    path('data/component_errors/<str:image_path>', views.component_error),
    #Create a new job and specify all panels with 'panels[0]panel_photo : file' etc
    path('api/createjob', views.JobCreate.as_view(), name='create_job'),
    #Update False Positive Error
    path('api/error_update/<int:pk>', views.ErrorUpdate.as_view(), name='error_update'),
    #Get all helpful errors back
    path('api/error_list', views.ErrorList.as_view(), name="error_list"),
    #Delete the specified job and all its children
    path('api/job_delete/<int:pk>', views.JobDelete.as_view(), name='job_delete')
]