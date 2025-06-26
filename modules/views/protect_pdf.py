import os
from io import BytesIO
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from PyPDF2 import PdfReader, PdfWriter
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class ProtectPDFView(View):
    template_name = 'protect_pdf.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pdf_file = request.FILES.get('file')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        permission_level = request.POST.get('permission_level')

        if not pdf_file:
            return render(request, self.template_name, {'error': 'Please upload a PDF file.'})

        if pdf_file.size > 100 * 1024 * 1024:
            return render(request, self.template_name, {'error': 'File must be less than 100MB.'})

        if not pdf_file.name.endswith('.pdf'):
            return render(request, self.template_name, {'error': 'Only PDF files are supported.'})

        if not password or not confirm_password:
            return render(request, self.template_name, {'error': 'Please enter and confirm the password.'})

        if password != confirm_password:
            return render(request, self.template_name, {'error': 'Passwords do not match.'})

        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            # PyPDF2's encrypt() does not support permission flags directly, so only password is set.
            # For advanced permissions use other libraries like pikepdf.
            writer.encrypt(user_pwd=password, owner_pwd=password)

            buffer = BytesIO()
            writer.write(buffer)
            buffer.seek(0)

            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="protected.pdf"'
            return response

        except Exception as e:
            return render(request, self.template_name, {'error': f'Error processing PDF: {str(e)}'})