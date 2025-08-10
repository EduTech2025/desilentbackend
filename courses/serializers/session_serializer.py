from rest_framework import serializers
from courses.models.course_model import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
