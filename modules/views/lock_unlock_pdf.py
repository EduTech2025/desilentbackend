
import re
from io import BytesIO
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from PyPDF2 import PdfReader, PdfWriter
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class LockUnlockPDFView(View):
    template_name = 'lock_unlock_pdf.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pdf_file = request.FILES.get('pdf_file')
        action = request.POST.get('action')  # 'lock' or 'unlock'
        password = request.POST.get('password')

        if not pdf_file:
            return JsonResponse({'error': 'No PDF uploaded'}, status=400)

        if action not in ['lock', 'unlock']:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        try:
            reader = PdfReader(pdf_file)

            if action == 'unlock':
                if reader.is_encrypted:
                    if not password:
                        return JsonResponse({'error': 'PDF is encrypted. Password required.'}, status=400)
                    if not reader.decrypt(password):
                        return JsonResponse({'error': 'Incorrect password. Cannot unlock.'}, status=400)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)

                buffer = BytesIO()
                writer.write(buffer)
                buffer.seek(0)

                return HttpResponse(buffer, content_type='application/pdf', headers={
                    'Content-Disposition': 'attachment; filename="unlocked.pdf"'
                })

            elif action == 'lock':
                if reader.is_encrypted:
                    return JsonResponse({'error': 'File already protected. Unlock first.'}, status=400)
                if not password:
                    return JsonResponse({'error': 'Please enter password to protect PDF.'}, status=400)

                # Password strength check
                strength = "weak"
                if len(password) >= 8 and re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"[0-9]", password) and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                    strength = "strong"
                elif len(password) >= 6:
                    strength = "medium"

                print(f"Password strength: {strength}")  # Optional logging

                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)

                writer.encrypt(password)

                buffer = BytesIO()
                writer.write(buffer)
                buffer.seek(0)

                return HttpResponse(buffer, content_type='application/pdf', headers={
                    'Content-Disposition': 'attachment; filename="locked.pdf"'
                })

        except Exception as e:
            return JsonResponse({'error': f'Processing failed: {str(e)}'}, status=500)
