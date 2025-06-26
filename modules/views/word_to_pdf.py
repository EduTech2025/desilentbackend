# import os
# import uuid
# from io import BytesIO
# from PIL import Image as PILImage

# from django.views import View
# from django.shortcuts import render
# from django.core.files.storage import default_storage
# from django.http import FileResponse

# # from pptx import Presentation
# # from pptx.enum.shapes import MSO_SHAPE_TYPE

# # from docx2pdf import convert as docx2pdf_convert
# # from comtypes import CoInitialize, CoUninitialize

# import comtypes.client

# class WordAndPPTToPDFView(View):
#     template_name = 'word_to_pdf.html'
#     word_exts = ['.docx']
#     ppt_exts = ['.pptx']
#     max_size = 20 * 1024 * 1024  # 10MB limit

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         uploaded_file = request.FILES.get('file')
#         file_type = request.POST.get('file_type')

#         if not uploaded_file:
#             return render(request, self.template_name, {"error": "No file uploaded."})

#         ext = os.path.splitext(uploaded_file.name)[-1].lower()
#         if uploaded_file.size > self.max_size:
#             return render(request, self.template_name, {"error": "File exceeds 10MB limit."})

#         if file_type == "word" and ext not in self.word_exts:
#             return render(request, self.template_name, {"error": "Only .docx files supported for Word."})
#         if file_type == "ppt" and ext not in self.ppt_exts:
#             return render(request, self.template_name, {"error": "Only .pptx files supported for PPT."})

#         temp_name = f"{uuid.uuid4()}{ext}"
#         input_path = default_storage.save(f"temp/{temp_name}", uploaded_file)
#         full_input_path = default_storage.path(input_path)
#         output_path = full_input_path.replace(ext, ".pdf")

#         # try:
#         #     if file_type == "word":
#         #         try:
#         #             # CoInitialize()
#         #             # docx2pdf_convert(full_input_path, output_path)
#         #         finally:
#         #             # CoUninitialize()

#         #     elif file_type == "ppt":
#         #         try:
#         #             # CoInitialize()
#         #             powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
#         #             powerpoint.Visible = 1
#         #             presentation = powerpoint.Presentations.Open(full_input_path, WithWindow=False)
#         #             presentation.SaveAs(output_path, 32)  # 32 = ppSaveAsPDF
#         #             presentation.Close()
#         #             powerpoint.Quit()
#         #         finally:
#         #             # CoUninitialize()

#         return FileResponse(open(output_path, 'rb'), as_attachment=True, filename=os.path.basename(output_path))

#         # except Exception as e:
#         #     return render(request, self.template_name, {"error": f"Conversion failed: {str(e)}"})
#         # finally:
#         #     try:
#         #         os.remove(full_input_path)
#         #     except:
#         #         pass
