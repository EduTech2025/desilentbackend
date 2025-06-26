# File: modules/views/pdf_rotator_tool.py

import io, zipfile
from PyPDF2 import PdfReader, PdfWriter
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class PDFRotateView(View):
    def get(self, request):
        return render(request, 'rotate_pdf.html')

    def post(self, request):
        files = request.FILES.getlist('pdf_files')
        rotate_type = request.POST.get('rotate_type')  # "all" or "specific"
        rotate_angle = int(request.POST.get('rotate_angle', 90))
        page_data = request.POST.get('page_data')  # "0:90,2:180" if specific

        file_streams = []

        for pdf_file in files:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            total_pages = len(reader.pages)

            for i in range(total_pages):
                page = reader.pages[i]
                if rotate_type == 'all':
                    page.rotate(rotate_angle)
                elif rotate_type == 'specific' and page_data:
                    rotations = {
                        int(k): int(v) for k, v in 
                        (pair.split(':') for pair in page_data.split(',') if ':' in pair)
                    }
                    if i in rotations:
                        page.rotate(rotations[i])
                writer.add_page(page)

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            file_streams.append((pdf_file.name, output))

        if len(file_streams) == 1:
            response = HttpResponse(file_streams[0][1], content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=rotated_{file_streams[0][0]}'
        else:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for name, stream in file_streams:
                    zip_file.writestr(f'rotated_{name}', stream.read())
            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=rotated_pdfs.zip'

        return response
