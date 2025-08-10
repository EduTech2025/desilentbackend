from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from courses.models.course_model import Feedback
from courses.serializers.feedback_serializer import FeedbackSerializer

class FeedbackView(APIView):

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        student_id = request.query_params.get('student_id', '').strip()
        feedbacks = Feedback.objects.all()
        if student_id:
            feedbacks = feedbacks.filter(student_id=student_id)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        pk = request.data.get('feedback_id')
        if not pk:
            return Response({"error": "feedback_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        feedback = get_object_or_404(Feedback, pk=pk)
        serializer = FeedbackSerializer(feedback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.data.get('feedback_id')
        if not pk:
            return Response({"error": "feedback_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        feedback = get_object_or_404(Feedback, pk=pk)
        feedback.delete()
        return Response({"message": f"Feedback {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)
