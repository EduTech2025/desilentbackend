import io
import pdfplumber
from openpyxl import Workbook
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class PDFToExcelView(View):

    def get(self, request):
        # Render HTML form for uploading PDF
        return render(request, 'pdf_to_excel.html')

    def post(self, request):
        pdf_file = request.FILES.get('file')
        if not pdf_file:
            return HttpResponse("No PDF file uploaded.", status=400)

        tables = []
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                tables.extend(page_tables)

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Extracted Table"

        row_index = 1
        for table in tables:
            for row in table:
                for col_index, cell in enumerate(row, start=1):
                    sheet.cell(row=row_index, column=col_index).value = cell
                row_index += 1
            row_index += 1

        excel_buffer = io.BytesIO()
        workbook.save(excel_buffer)
        excel_buffer.seek(0)

        response = HttpResponse(
            excel_buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="output.xlsx"'
        return response
