from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from courses.models.course_model import ProjectSubmission
from courses.serializers.project_serializer import ProjectSubmissionSerializer

class ProjectSubmissionAPI(APIView):

    def post(self, request):
        data = request.data
        is_many = isinstance(data, list)

        serializer = ProjectSubmissionSerializer(data=data, many=is_many)

        if serializer.is_valid():
         serializer.save()
         return Response({
            "message": "Projects submitted successfully" if is_many else "Project submitted successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

        print("❌ Validation Error:", serializer.errors)  # 👈 Add this
        return Response({
        "message": "Validation failed",
        "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request):
       student_id = request.query_params.get('student')  # ✅ This works for GET
       if student_id:
        submissions = ProjectSubmission.objects.filter(student=student_id)
       else:
        submissions = ProjectSubmission.objects.all()
       serializer = ProjectSubmissionSerializer(submissions, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request):
        project_id = request.data.get('project_id')
        try:
            submission = ProjectSubmission.objects.get(project_id=project_id)
        except ProjectSubmission.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSubmissionSerializer(submission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Project updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        project_id = request.data.get('project_id')
        try:
            submission = ProjectSubmission.objects.get(project_id=project_id)
            submission.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_200_OK)
        except ProjectSubmission.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
