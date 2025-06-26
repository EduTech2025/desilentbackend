from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

class OrganizePDFView(View):
    template_name = 'organize_pdf.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        uploaded_pdf = request.FILES.get('pdf_file')
        if not uploaded_pdf:
            return HttpResponse("No file uploaded", status=400)

        reader = PdfReader(uploaded_pdf)
        writer = PdfWriter()

        page_order = request.POST.getlist('page_order[]')
        rotations = request.POST.getlist('rotations[]')
        deletes = request.POST.getlist('deletes[]')

        for i in range(len(page_order)):
            index = page_order[i]
            rotate = rotations[i]
            delete = deletes[i]

            if delete == 'true':
                continue

            # ✅ Support dynamic blank page ID
            if index.startswith("blank"):
                first_page = reader.pages[0]
                width = float(first_page.mediabox.width)
                height = float(first_page.mediabox.height)
                writer.add_blank_page(width=width, height=height)
                continue

            try:
                idx = int(index)
                page = reader.pages[idx]
                angle = int(rotate)

                if angle != 0:
                    page.rotate(angle)
                writer.add_page(page)

            except (ValueError, IndexError):
                continue  # skip broken entries

        output = BytesIO()
        writer.write(output)
        output.seek(0)

        response = HttpResponse(output, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="organized.pdf"'
        return response
