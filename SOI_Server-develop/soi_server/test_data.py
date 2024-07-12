from io import BytesIO
from os import stat
from django.core.files.base import ContentFile
from inspector.models import Error, Job, Panel
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




def create_testdata():
    cnf = SimpleUploadedFile('test.json', b'config', content_type="json")
    pos = SimpleUploadedFile('test.csv', b'pos', content_type="csv")
    img = SimpleUploadedFile('test.png', (create_image(None, 'test.png')).getvalue(), content_type="image/png")
    job = Job.objects.create(name='test', config=cnf, position=pos)
    job.save()

    panel = Panel.objects.create(job=job, panel_photo=img)
    panel.save()

    # board = Board.objects.create(panel=panel, board_image=img)
    # board.save()

    error = Error.objects.create(panel_id=panel, component_name='CXX', component_image=img, coordinate_x=566, coordinate_y=344, helpful=False, designator='TTU')
    error.save()




