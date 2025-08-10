from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from dashboard.models import Message
from dashboard.serializer.chat_serializer import MessageSerializer
import datetime

class SaveMessageView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            timestamp = datetime.datetime.fromtimestamp(data['timestamp'] / 1000.0)
            data['timestamp'] = timestamp

            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'saved'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MarkMessagesReadView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)

        updated = Message.objects.filter(receiver_id=user_id, read=False).update(
            read=True,
            read_at=timezone.now()
        )
        return Response({'status': 'updated', 'count': updated}, status=status.HTTP_200_OK)
