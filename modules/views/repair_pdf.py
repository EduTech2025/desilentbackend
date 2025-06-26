import os
import tempfile
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from django.http import FileResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@method_decorator(csrf_exempt, name='dispatch')
class RepairPDFView(View):
    template_name = 'repair_pdf.html'
    max_file_size = 50 * 1024 * 1024  # 50MB

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pdf_file = request.FILES.get('pdf_file')
        if not pdf_file:
            return HttpResponse("No file uploaded", status=400)

        if pdf_file.size > self.max_file_size:
            return HttpResponse("File size exceeds 50MB limit.", status=400)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        temp_dir = tempfile.gettempdir()

        input_path = os.path.join(temp_dir, f'input_{timestamp}.pdf')
        output_path = os.path.join(temp_dir, f'repaired_{timestamp}.pdf')

        # Save uploaded file temporarily
        with open(input_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            with open(output_path, 'wb') as f:
                writer.write(f)

            return FileResponse(open(output_path, 'rb'), content_type='application/pdf', as_attachment=True, filename='repaired.pdf')

        except Exception as e:
            return HttpResponse(f"Failed to repair PDF: {e}", status=500)

        finally:
            try:
                os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
            except Exception:
                pass
