from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from courses.models.course_model import Comment
from courses.serializers.comment_serializer import CommentSerializer

class CommentView(APIView):
    def post(self, request):
        data = request.data
        is_many = isinstance(data, list)
        serializer = CommentSerializer(data=data, many=is_many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        query = request.query_params.get('search', '').strip().lower()
        comments = Comment.objects.all()

        if query:
            comments = comments.filter(
                Q(user_name__icontains=query) | 
                Q(email__icontains=query) | 
                Q(comment__icontains=query)
            )

        return Response(CommentSerializer(comments, many=True).data)

    def put(self, request):
        pk = request.data.get('comment_id')
        if not pk:
            return Response({"error": "comment_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.data.get('comment_id')
        if not pk:
            return Response({"error": "comment_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({"message": f"Comment {pk} deleted."}, status=status.HTTP_204_NO_CONTENT)
