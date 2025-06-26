import os
import zipfile
import tempfile
from datetime import datetime
import fitz  # PyMuPDF
from django.http import FileResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@method_decorator(csrf_exempt, name='dispatch')
class PDFToImagesView(View):

    template_name = 'pdf_to_images.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pdf_file = request.FILES.get('pdf_file')
        if not pdf_file:
            return HttpResponse("No file uploaded", status=400)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        temp_dir = tempfile.gettempdir()

        input_path = os.path.join(temp_dir, f'input_{timestamp}.pdf')
        zip_path = os.path.join(temp_dir, f'images_{timestamp}.zip')

        # Save PDF temporarily
        with open(input_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        try:
            doc = fitz.open(input_path)
            image_paths = []

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                image_path = os.path.join(temp_dir, f'page_{timestamp}_{page_num+1}.png')
                pix.save(image_path)
                image_paths.append(image_path)

            if not image_paths:
                return HttpResponse("No images generated", status=500)

            # Create ZIP of images
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for img_path in image_paths:
                    zipf.write(img_path, arcname=os.path.basename(img_path))

            return FileResponse(open(zip_path, 'rb'), content_type='application/zip', as_attachment=True, filename='converted_images.zip')

        except Exception as e:
            return HttpResponse(f"Error processing PDF: {e}", status=500)

        finally:
            # Clean up
            try:
                os.remove(input_path)
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                for img in image_paths:
                    os.remove(img)
            except Exception:
                pass
