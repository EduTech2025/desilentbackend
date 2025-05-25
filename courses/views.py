from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Session, Comment
from .serializers import CourseSerializer, SessionSerializer, CommentSerializer

# -------- COURSE VIEWS --------
@api_view(['GET', 'POST'])
def course_list_create(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, course_id):
    try:
        course = Course.objects.get(course_id=course_id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)

    if request.method == 'GET':
        return Response(CourseSerializer(course).data)
    elif request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        course.delete()
        return Response(status=204)


# -------- SESSION VIEWS --------
@api_view(['GET', 'POST'])
def session_list_create(request):
    if request.method == 'GET':
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def session_detail(request, session_id):
    try:
        session = Session.objects.get(session_id=session_id)
    except Session.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

    if request.method == 'GET':
        return Response(SessionSerializer(session).data)
    elif request.method == 'PUT':
        serializer = SessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        session.delete()
        return Response(status=204)


# -------- COMMENT VIEWS --------
@api_view(['GET', 'POST'])
def comment_list_create(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_id):
    try:
        comment = Comment.objects.get(comment_id=comment_id)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=404)

    if request.method == 'GET':
        return Response(CommentSerializer(comment).data)
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=204)
