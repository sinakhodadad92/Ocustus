from os import error
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http.response import HttpResponse


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response

from .models import Error, Job, Panel
from .serializers import ErrorSerializer, JobSerializer, JobListSerializer, JobCreateSerializer, ErrorUpdateSerializer

from threading import Thread

from error_detection.pipeline import run_with_paths

from PIL import Image

from django.core.files.base import ContentFile

from io import BytesIO


@api_view(['GET'])
def panel_image(request, image_path):
    """
    Save method for the panel images.
    Wrapper function
    """
    return job_images(request, 'data/panel_images/', image_path)

@api_view(['GET'])
def cropped_panel_image(request, image_path):
    """
    Save method for the panel images.
    Wrapper function
    """
    return job_images(request, 'data/cropped_panel_images/', image_path)

@api_view(['GET'])
def component_error(request, image_path):
    """
    Save method for the panel images.
    Wrapper function
    """
    return job_images(request, 'data/component_errors/', image_path)


def job_images(request, prefex, image_path):
    """
    This method is used to save images
    """
    if request.method == 'GET':
        try:
            with open(prefex + image_path, 'rb') as f:
                return HttpResponse(f.read(), content_type='image/jpg')
        except IOError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class JobList(generics.ListAPIView):
    """
    This view returns all created jobs via a GET request.
    The JobListSerializer is used to serialize the objects. 
    """
    queryset = Job.objects.all()
    serializer_class = JobListSerializer


class JobDetail(generics.RetrieveAPIView):
    """
    Unlike JobList, here for a given job (defined by its id) all 
    associated models are returned. 
    The JobSerializer is used for this purpose.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobCreate(generics.CreateAPIView):
    """    
    This view is used for the creation of a job 
    and at the same time the panels are saved. 
    The JobCreateSerializer is used for this purpose.
    Also in the create function the error detection 
    pipline gets called as a thread.
    """
    serializer_class = JobCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Call the Thread for the error detection
        job_id = (serializer.data)['id']
        thread = Thread(target=perform_error_detection_thread,
                        daemon=True, args=[job_id])
        thread.start()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class JobDelete(generics.DestroyAPIView):
    """
    For a given Job id the job gets deleted and all
    its child elements on the database which means errors etc.
    """
    queryset = Job.objects.all()
    serializer_class = JobListSerializer

    #Make sure to delete all files to not pollute server.
    #The files are saved in a folder.
    def delete(self, request, *args, **kwargs):
        try:
            job = Job.objects.get(id=kwargs['pk'])
            panels = job.panels.all()
            
            for panel in panels:
                errors = panel.error_set.all()

                for error in errors:
                    error.delete()

                panel.delete()

            return super().delete(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return super().delete(request, *args, **kwargs)


class ErrorUpdate(generics.UpdateAPIView):
    """
    This class updates the state of the errors boolean value
    to show if its a false positive or true positive.
    """
    queryset = Error.objects.all()
    serializer_class = ErrorUpdateSerializer


class ErrorList(generics.ListAPIView):
    """
    Give back all errors in one list, 
    but filtered out the False Positives.
    """
    serializer_class = ErrorSerializer

    def get_queryset(self):
        return Error.objects.filter(rework=True)


def perform_error_detection_thread(job_id):
    """
    Server side Wrapper for the error detection pipline.
    First call run_with_paths which will call the actuall 
    error detection and get back the errors. After that
    the functions save_component_errors and
    save_cropped_panel_image will save the results.
    """
    job = Job.objects.get(id=job_id)
    try:
        config_path = job.config.path
        position_path = job.position.path
        panel_img_path_arr = []
        for panel in job.panels.all():
            pan_id = panel.id
            pan_path = panel.panel_photo.path
            panel_img_path_arr.append((pan_id, pan_path))

        result = run_with_paths(panel_img_path_arr, config_path, position_path)

        # save output of the error function
        save_component_errors(result['components'])
        save_cropped_panel_images(result['cropped_panels'])
        job.job_state = 'COMPLETED'
        job.save()
    except Exception as e:
        print(e)
        job.job_state = 'FAILED'
        job.save()

    # save output of the error function


def save_component_errors(components):
    """
    Save all errors which where detected in the error detection 
    to the corresponding board and panel
    """
    i = 0
    for component in components:
        i += 1
        error_list = component['errors']
        for error in error_list:
            panel = Panel.objects.get(id=error['panel_id'])
            img_io = BytesIO()
            error['img'].save(img_io, format='JPEG', quality=100)
            img_content = ContentFile(
                img_io.getvalue(), 'component_' + str(error['panel_id']) + '_' + str(i) + '_.jpg')
            errorObj = Error.objects.create(
                panel_id=panel, board_id=error['board_id'], component_image=img_content,
                designator=component['designator'], coordinate_x=error['coordinates'][0], coordinate_y=error['coordinates'][1],
                component_value=component['component_value'])
            errorObj.save()


def save_cropped_panel_images(cropped_panels):
    """
    Save the cropped panel image to the corresponding
    panel.
    """
    for cropped_panel in cropped_panels:
        panel = Panel.objects.get(id=cropped_panel['id'])
        img_io = BytesIO()
        cropped_panel['img'].save(img_io, format='JPEG', quality=100)
        cropped_panel_photo_name = panel.panel_photo.url.split(
            "/")[-1].removesuffix('.jpg') + '_cropped.jpg'
        img_content = ContentFile(
            img_io.getvalue(), cropped_panel_photo_name)
        panel.cropped_panel_photo = img_content
        panel.save()
