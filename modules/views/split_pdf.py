import os
import tempfile
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
import fitz  # PyMuPDF

@method_decorator(csrf_exempt, name='dispatch')
class SplitPDFView(View):
    template_name = 'split_pdf.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        file = request.FILES.get('pdf_file')
        split_mode = request.POST.get('split_mode')
        range_input = request.POST.get('range_input', '')
        selected_pages = request.POST.get('selected_pages', '')

        if not file or file.size > 100 * 1024 * 1024:
            return HttpResponse("Invalid or too large file", status=400)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        temp_input = os.path.join(tempfile.gettempdir(), f"split_input_{timestamp}.pdf")
        output_file = os.path.join(tempfile.gettempdir(), f"split_output_{timestamp}.pdf")

        with open(temp_input, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        try:
            reader = PdfReader(temp_input)
            writer = PdfWriter()

            if split_mode == 'range':
                for part in range_input.split(','):
                    start, end = map(int, part.strip().split('-'))
                    for i in range(start - 1, end):
                        writer.add_page(reader.pages[i])
            else:  # specific pages
                pages = [int(p) - 1 for p in selected_pages.split(',') if p.isdigit()]
                for i in pages:
                    writer.add_page(reader.pages[i])

            with open(output_file, 'wb') as f:
                writer.write(f)

            return FileResponse(open(output_file, 'rb'), as_attachment=True, filename="split_result.pdf")

        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

        finally:
            try:
                os.remove(temp_input)
                if os.path.exists(output_file):
                    os.remove(output_file)
            except:
                pass

# Separate view to generate previews
@csrf_exempt
def preview_pages(request):
    file = request.FILES.get('pdf_file')
    if not file or file.size > 100 * 1024 * 1024:
        return JsonResponse({"error": "Invalid or large file"}, status=400)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    temp_input = os.path.join(tempfile.gettempdir(), f"preview_input_{timestamp}.pdf")
    preview_dir = os.path.join(tempfile.gettempdir(), f"preview_pages_{timestamp}")
    os.makedirs(preview_dir, exist_ok=True)

    with open(temp_input, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    doc = fitz.open(temp_input)
    pages = []
    for i in range(len(doc)):
        img_path = os.path.join(preview_dir, f"page_{i+1}.png")
        pix = doc[i].get_pixmap()
        pix.save(img_path)
        pages.append(f"/media/previews/{os.path.basename(img_path)}")

    return JsonResponse({"pages": pages})
