from django.views import View
from django.http import HttpResponse, JsonResponse
from pypdf import PdfWriter, PdfReader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import io

@method_decorator(csrf_exempt, name='dispatch')
class MergePDFsView(View):
    def post(self, request):
        files = request.FILES.getlist('pdfs')

        if not files or len(files) < 2:
            return JsonResponse({'error': 'Please upload at least two PDF files.'}, status=400)

        writer = PdfWriter()

        try:
            for uploaded_file in files:
                uploaded_file.seek(0)  # very important!
                pdf_bytes = uploaded_file.read()
                file_stream = io.BytesIO(pdf_bytes)
                file_stream.seek(0)

                reader = PdfReader(file_stream)

                if len(reader.pages) == 0:
                    return JsonResponse({'error': f'{uploaded_file.name} has 0 pages or could not be read'}, status=400)

                for page in reader.pages:
                    writer.add_page(page)

            output_stream = io.BytesIO()
            writer.write(output_stream)
            output_stream.seek(0)

            response = HttpResponse(output_stream.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
            return response

        except Exception as e:
            return JsonResponse({'error': f'Failed to merge PDFs: {str(e)}'}, status=500)
