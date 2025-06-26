from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import tempfile, os

@method_decorator(csrf_exempt, name='dispatch')
class AddWatermarkToPDF(View):
    template_name = 'add_watermark.html'

    def get(self, request):
     return render(request, self.template_name, {
        'opacity_values': ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8'],
        'rotation_values': ['0', '30', '45', '60', '90', '120', '150', '180']
    })

 
    def post(self, request):
        pdf_file = request.FILES.get('pdf_file')
        watermark_type = request.POST.get('watermark_type')
        watermark_text = request.POST.get('watermark_text')
        watermark_image = request.FILES.get('watermark_image')
        base_font = request.POST.get('font_name', 'Helvetica')
        font_size = int(request.POST.get('font_size', '40'))
        opacity = float(request.POST.get('opacity', '0.3'))
        rotation = int(request.POST.get('rotation', '0'))
        position = request.POST.get('position', 'middle-center')
        page_range = request.POST.get('page_range', '')
        mosaic = request.POST.get('mosaic') == 'on'

        font_name = base_font
        if base_font == 'Helvetica':
            if 'bold' in request.POST and 'italic' in request.POST:
                font_name = 'Helvetica-BoldOblique'
            elif 'bold' in request.POST:
                font_name = 'Helvetica-Bold'
            elif 'italic' in request.POST:
                font_name = 'Helvetica-Oblique'
        elif base_font == 'Courier':
            if 'bold' in request.POST and 'italic' in request.POST:
                font_name = 'Courier-BoldOblique'
            elif 'bold' in request.POST:
                font_name = 'Courier-Bold'
            elif 'italic' in request.POST:
                font_name = 'Courier-Oblique'
        elif base_font == 'Times-Roman':
            if 'bold' in request.POST and 'italic' in request.POST:
                font_name = 'Times-BoldItalic'
            elif 'bold' in request.POST:
                font_name = 'Times-Bold'
            elif 'italic' in request.POST:
                font_name = 'Times-Italic'
            else:
                font_name = 'Times-Roman'

        if not pdf_file:
            return HttpResponse("PDF is required.", status=400)
        if watermark_type == 'text' and not watermark_text:
            return HttpResponse("Watermark text is required.", status=400)
        if watermark_type == 'image' and not watermark_image:
            return HttpResponse("Watermark image is required.", status=400)

        def parse_page_range(page_range, total_pages):
            if not page_range.strip():
                return list(range(total_pages))
            selected = set()
            for part in page_range.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    selected.update(range(start-1, end))
                else:
                    selected.add(int(part)-1)
            return sorted([i for i in selected if 0 <= i < total_pages])

        def get_position_coords(pos, width, height):
            pos_map = {
                'top-left': (100, height - 100),
                'top-center': (width / 2, height - 100),
                'top-right': (width - 100, height - 100),
                'middle-left': (100, height / 2),
                'middle-center': (width / 2, height / 2),
                'middle-right': (width - 100, height / 2),
                'bottom-left': (100, 100),
                'bottom-center': (width / 2, 100),
                'bottom-right': (width - 100, 100),
            }
            return pos_map.get(pos, (width / 2, height / 2))

        def create_watermark_page(page_width, page_height):
            packet = BytesIO()
            c = canvas.Canvas(packet, pagesize=(page_width, page_height))
            c.setFillAlpha(opacity)
            c.saveState()
            c.translate(page_width / 2, page_height / 2)
            c.rotate(rotation)
            c.translate(-page_width / 2, -page_height / 2)

            if watermark_type == 'text':
                try:
                    c.setFont(font_name, font_size)
                except:
                    c.setFont("Helvetica", font_size)
                    print(f"⚠️ Font '{font_name}' not found. Defaulted to Helvetica.")

                x, y = get_position_coords(position, page_width, page_height)
                if mosaic:
                    for i in range(0, int(page_width), 200):
                        for j in range(0, int(page_height), 100):
                            c.drawString(i, j, watermark_text)
                else:
                    c.drawCentredString(x, y, watermark_text)
                    if 'underline' in request.POST:
                        text_width = c.stringWidth(watermark_text, font_name, font_size)
                        underline_y = y - 2
                        c.line(x - text_width/2, underline_y, x + text_width/2, underline_y)

            else:
                image = Image.open(watermark_image)
                image.thumbnail((200, 200))
                img_path = tempfile.mktemp(suffix=".png")
                image.save(img_path)
                x, y = get_position_coords(position, page_width, page_height)
                if mosaic:
                    for i in range(0, int(page_width), 200):
                        for j in range(0, int(page_height), 200):
                            c.drawImage(img_path, i, j, mask='auto')
                else:
                    c.drawImage(img_path, x - 100, y - 100, mask='auto')
                os.remove(img_path)

            c.restoreState()
            c.save()
            packet.seek(0)
            return PdfReader(packet).pages[0]

        pdf_reader = PdfReader(pdf_file)
        pdf_writer = PdfWriter()
        target_pages = parse_page_range(page_range, len(pdf_reader.pages))

        for idx, page in enumerate(pdf_reader.pages):
            if idx in target_pages:
                width = float(page.mediabox.width)
                height = float(page.mediabox.height)
                watermark = create_watermark_page(width, height)
                page.merge_page(watermark)
            pdf_writer.add_page(page)

        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)

        response = HttpResponse(output, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="watermarked_output.pdf"'
        return response
