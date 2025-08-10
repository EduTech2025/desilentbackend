from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from courses.models.course_model import Course
from courses.serializers.course_serializer import CourseSerializer


class CourseView(APIView):

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        name = request.query_params.get('name', '').strip().lower()
        updated_by = request.query_params.get('updated_by', '').strip().lower()

        courses = Course.objects.all()

        if name:
            courses = courses.filter(Q(course_name__icontains=name) | Q(description__icontains=name))

        if updated_by:
            courses = courses.filter(updated_by__icontains=updated_by)

        return Response(CourseSerializer(courses, many=True).data, status=status.HTTP_200_OK)

    def put(self, request):
        pk = request.data.get('course_id')
        if not pk:
            return Response({"error": "Primary key 'course_id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.data.get('course_id')
        if not pk:
            return Response({"error": "Primary key 'course_id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response({"message": f"Course with ID {pk} deleted."}, status=status.HTTP_204_NO_CONTENT)
