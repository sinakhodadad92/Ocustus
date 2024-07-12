from django.db import models

# Create your models here.
class Job(models.Model):
    """
    The Job is the central element of every Job workflow.
    It holds all the nesseccary information to identify all panels
    corresponding to this job. Each Job is a Collection of panels with
    the same properties in there configuration and position of electronical components. 
    """
    IN_PROGRESS = 'PROCESSING'
    FAILED = 'FAILED'
    COMPLETED = 'COMPLETED'
    JOB_STATE = [
        (IN_PROGRESS, 'In_progress'),
        (FAILED, 'Failed'),
        (COMPLETED, 'Completed'),
    ]
    job_state = models.CharField(max_length=10, choices=JOB_STATE,default=IN_PROGRESS)
    name = models.CharField(max_length=50)
    config = models.FileField(upload_to='data/configs/')
    position = models.FileField(upload_to='data/positions/')

    def delete(self, using=None, keep_parents=False):
        self.config.storage.delete(self.config.name)
        self.position.storage.delete(self.position.name)
        super().delete()

class Panel(models.Model):
    """
    The panel is characterized by its job information (parent) and panel photo.
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='panels')
    panel_photo = models.ImageField(upload_to='data/panel_images/')
    cropped_panel_photo = models.ImageField(upload_to='data/cropped_panel_images/',null=True, default=None)

    def delete(self, using=None, keep_parents=False):
        self.panel_photo.storage.delete(self.panel_photo.name)
        self.cropped_panel_photo.storage.delete(self.cropped_panel_photo.name)
        super().delete()


class Error(models.Model):
    """
    The error is what we call a potentially defect part of the panel.
    It can be seen as an panel error, we save for each error the positions, if it needs
    to get reworked etc."""
    designator = models.CharField(max_length=50)
    rework = models.BooleanField(default=True)
    coordinate_x = models.IntegerField(null=True, default=None)
    coordinate_y = models.IntegerField(null=True, default=None)
    component_image = models.ImageField(upload_to='data/component_errors/')
    component_value = models.CharField(max_length=150, null=True, default=None)
    panel_id = models.ForeignKey(Panel,on_delete=models.CASCADE)
    board_id = models.IntegerField()

    def delete(self, using=None, keep_parents=False):
        self.component_image.storage.delete(self.component_image.name)
        super().delete()




