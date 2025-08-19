from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.parsers import JSONParser

class ContactAPIView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        data = request.data
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        if not all([name, email, subject, message]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        full_message = f"""
        You have received a new message from your website contact form:

        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        try:
            send_mail(
                subject=f'Contact Form: {subject}',
                message=full_message,
                from_email=email,
                recipient_list=['desilentorder@proton.me','support@desilentorder.in'],
                fail_silently=False,
            )
            return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to send email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
