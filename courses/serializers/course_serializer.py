from rest_framework import serializers
from courses.models.course_model import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
