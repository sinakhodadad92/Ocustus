from .models import Job, Panel, Error
from rest_framework import serializers

#Those serializers are the parts which will convert the jsons of a request to a 
#object in the database those are mapping classes, which ensure validation of the data, 
#creation of the database objects and saving of the objects into the database.

class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Error
        fields = '__all__'

class PanelSerializer(serializers.ModelSerializer):
    errors = ErrorSerializer(read_only=True, source='error_set', many=True)
    class Meta:
        model = Panel
        fields = ['errors', 'panel_photo', 'cropped_panel_photo','id']

class PanelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panel
        fields = ['panel_photo']

class JobSerializer(serializers.ModelSerializer):
    panels = PanelSerializer(read_only=True,many=True)
    class Meta:
        model = Job
        fields = "__all__"

class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

class JobCreateSerializer(serializers.ModelSerializer):
    panels = PanelCreateSerializer(many=True)

    class Meta:
        model = Job
        fields = ['id','name', 'config', 'position', 'panels']

    def create(self, validated_data):
        panels = validated_data.pop('panels')
        job = Job.objects.create(**validated_data)
        for panel in panels:
            Panel.objects.create(job=job, **panel)

        return job

class ErrorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Error
        fields = ['rework']