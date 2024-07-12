from io import BytesIO
from os import stat
from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inspector.views import ErrorList
from .models import Error, Job, Panel
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

from django.conf import settings
base_dir = settings.BASE_DIR

def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
   """
   Generate a test image, returning the filename that it was saved as.

   If ``storage`` is ``None``, the BytesIO containing the image data
   will be passed instead.
   """
   data = BytesIO()
   Image.new(image_mode, size).save(data, image_format)
   data.seek(0)
   if not storage:
       return data
   image_file = ContentFile(data.read())


class JobTests(APITestCase):
    def test_create_list_job(self):
        """
        Ensure we can create a new job object.
        """

        cnf = SimpleUploadedFile('test.json', b'config', content_type="json")
        pos = SimpleUploadedFile('test.csv', b'pos', content_type="csv")
        img = SimpleUploadedFile('test.png', (create_image(None, 'test.png')).getvalue(), content_type="image/png")
        img2 = SimpleUploadedFile('test2.jpg', (create_image(None, 'test.jpg')).getvalue(), content_type="image/jpg")

        job_name = 'TESTJOB'
        url = reverse('create_job')

        data = {'name' : job_name, 'config' : cnf, 'position' :  pos, 'panels[0]panel_photo' : img, 'panels[1]panel_photo' : img2}
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(Job.objects.get().name, job_name)
        self.assertEqual(Panel.objects.count(),2)

        url = reverse('job_list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(Job.objects.count(), len(data))

        job = (Job.objects.all())[0]
        job.delete()

    def test_board_analysis(self):
        cnf = SimpleUploadedFile('test.json', b'config', content_type="json")
        pos = SimpleUploadedFile('test.csv', b'pos', content_type="csv")
        img = SimpleUploadedFile('test.png', (create_image(None, 'test.png')).getvalue(), content_type="image/png")
        job = Job.objects.create(name='test', config=cnf, position=pos)
        job.save()

        panel = Panel.objects.create(job=job, panel_photo=img)
        panel.save()

        error = Error.objects.create(panel_id=panel, board_id=3,component_value='CXX', component_image=img, coordinate_x=566, coordinate_y=344, designator='TTU')
        error.save()

        url = reverse('job_detail', args=[job.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        job.delete()

    def test_update_error(self):
        cnf = SimpleUploadedFile('test.json', b'config', content_type="json")
        pos = SimpleUploadedFile('test.csv', b'pos', content_type="csv")
        img = SimpleUploadedFile('test.png', (create_image(None, 'test.png')).getvalue(), content_type="image/png")
        job = Job.objects.create(name='test', config=cnf, position=pos)
        job.save()

        panel = Panel.objects.create(job=job, panel_photo=img)
        panel.save()

        error = Error.objects.create(panel_id=panel, board_id=3,component_value='CXX', component_image=img, coordinate_x=566, coordinate_y=344, designator='TTU',rework=True)
        error.save()

        url = reverse('error_list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(Error.objects.filter(rework=True).count(), len(data))

        url = reverse('error_update', args=[error.id])
        response = self.client.put(url, {'rework' : 'False'}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rework'], False)

        url = reverse('error_list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(Error.objects.filter(rework=True).count(), len(data))

        job.delete()


