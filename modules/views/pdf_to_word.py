from django.shortcuts import render
from django.http import HttpResponse
from pdf2docx import Converter
import tempfile
import os

def pdf_to_word(request):
    if request.method == 'POST' and request.FILES.get('file'):
        pdf_file = request.FILES['file']

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_file.read())
            temp_pdf_path = temp_pdf.name

        temp_docx_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name

        try:
            cv = Converter(temp_pdf_path)
            cv.convert(temp_docx_path, start=0, end=None, layout=True)
            cv.close()

            with open(temp_docx_path, 'rb') as docx_file:
                response = HttpResponse(docx_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="converted.docx"'
                return response

        finally:
            os.remove(temp_pdf_path)
            os.remove(temp_docx_path)

    return render(request, 'pdf_to_word.html')
