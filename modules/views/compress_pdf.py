# modules/views/compress_pdf.py

from django.views import View
from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from io import BytesIO
import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class CompressPDFView(View):
    template_name = 'compress_pdf.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pdf_file = request.FILES.get('pdf_file')
        if not pdf_file or not pdf_file.name.lower().endswith('.pdf'):
            return JsonResponse({"error": "Invalid or missing PDF file."}, status=400)
        
        if pdf_file.content_type != 'application/pdf':
            return JsonResponse({"error": "Uploaded file is not a PDF."}, status=400)

        # Compression parameters
        compression_level = request.POST.get('quality', 'moderate').lower()
        greyscale = request.POST.get('greyscale', 'false').lower() == 'true'

        dpi_map = {
            'best': 144,
            'moderate': 100,
            'max': 72
        }
        dpi = dpi_map.get(compression_level, 100)

        try:
            input_pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
            output_pdf = fitz.open()

            logger.info(f"Processing {len(input_pdf)} pages with DPI={dpi}, Greyscale={greyscale}")

            for i, page in enumerate(input_pdf):
                try:
                    pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY if greyscale else fitz.csRGB)
                    img_bytes = pix.tobytes("jpeg")

                    rect = page.rect
                    new_page = output_pdf.new_page(width=rect.width, height=rect.height)
                    new_page.insert_image(rect, stream=img_bytes)
                except Exception as page_err:
                    logger.warning(f"Page {i + 1} skipped due to error: {page_err}")
                    continue

            input_pdf.close()

            if len(output_pdf) == 0:
                return JsonResponse({"error": "Compression failed: no valid pages processed."}, status=500)

            buffer = BytesIO()
            output_pdf.save(buffer, garbage=4, deflate=True)
            output_pdf.close()
            buffer.seek(0)

            original_size = pdf_file.size
            compressed_size = buffer.getbuffer().nbytes
            logger.info(f"Compression completed: {original_size} bytes → {compressed_size} bytes")

            return FileResponse(buffer, as_attachment=True, filename='compressed_output.pdf')

        except Exception as e:
            logger.error(f"Compression failed due to: {str(e)}")
            return JsonResponse({"error": f"Compression failed: {str(e)}"}, status=500)
