
import os
import tempfile
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from django.http import FileResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from io import BytesIO

@method_decorator(csrf_exempt, name='dispatch')
class AddPageNumberView(View):
    template_name = 'pagenumber_pdf.html'
    max_file_size = 100 * 1024 * 1024  # 100MB

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pdf_file = request.FILES.get('pdf_file')
        if not pdf_file:
            return HttpResponse("No file uploaded", status=400)
        if pdf_file.size > self.max_file_size:
            return HttpResponse("File size exceeds 100MB limit.", status=400)


        position = request.POST.get('position', 'bottom-right')
        page_range_input = request.POST.get('page_range', '')
        start_number = int(request.POST.get('start_number', 1))
        font_size = int(request.POST.get('font_size', 12))
        font_color = request.POST.get('font_color', '#000000')

        # Parse page range
        included_pages = set()
        if page_range_input:
            parts = page_range_input.split(',')
            for part in parts:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    included_pages.update(range(start - 1, end))
                else:
                    included_pages.add(int(part) - 1)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        temp_dir = tempfile.gettempdir()

        input_path = os.path.join(temp_dir, f'input_{timestamp}.pdf')
        output_path = os.path.join(temp_dir, f'numbered_{timestamp}.pdf')

        with open(input_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()
            total_pages = len(reader.pages)

            for i in range(total_pages):
                page = reader.pages[i]
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=letter)
                can.setFillColor(HexColor(font_color))
                can.setFont("Helvetica", font_size)

                if not included_pages or i in included_pages:
                    number = start_number + sorted(included_pages).index(i) if included_pages else start_number + i
                    x, y = self.get_position_coordinates(position, font_size)
                    can.drawString(x, y, str(number))

                can.save()
                packet.seek(0)
                overlay = PdfReader(packet)
                page.merge_page(overlay.pages[0])
                writer.add_page(page)

            with open(output_path, 'wb') as f:
                writer.write(f)

            return FileResponse(open(output_path, 'rb'), content_type='application/pdf', as_attachment=True, filename='numbered.pdf')

        except Exception as e:
            return HttpResponse(f"Failed to add page numbers: {e}", status=500)

        finally:
            try:
                os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
            except Exception:
                pass

    def get_position_coordinates(self, position, font_size):
        positions = {
            'top-left': (50, 770),
            'top-center': (270, 770),
            'top-right': (500, 770),
            'bottom-left': (50, 30),
            'bottom-center': (270, 30),
            'bottom-right': (500, 30)
        }
        return positions.get(position, (500, 30))

