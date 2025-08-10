from rest_framework import serializers
from courses.models.course_model import ProjectSubmission

class ProjectSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSubmission
        fields = '__all__'
