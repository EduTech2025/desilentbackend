from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from courses.models.course_model import Session
from courses.serializers.session_serializer import SessionSerializer


class SessionView(APIView):

    def post(self, request):
        data = request.data
        is_many = isinstance(data, list)
        serializer = SessionSerializer(data=data, many=is_many)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        session_name = request.query_params.get('session_name', '').strip()
        course_id = request.query_params.get('course_id', '').strip()

        sessions = Session.objects.all()

        if session_name:
            sessions = sessions.filter(session_name__icontains=session_name)
        if course_id:
            sessions = sessions.filter(course=course_id)

        return Response(SessionSerializer(sessions, many=True).data, status=status.HTTP_200_OK)

    def put(self, request):
        pk = request.data.get('session_id')
        if not pk:
            return Response({"error": "Primary key 'session_id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        session = get_object_or_404(Session, pk=pk)
        serializer = SessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.data.get('session_id')
        if not pk:
            return Response({"error": "Primary key 'session_id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        session = get_object_or_404(Session, pk=pk)
        session.delete()
        return Response({"message": f"Session with ID {pk} deleted."}, status=status.HTTP_204_NO_CONTENT)
