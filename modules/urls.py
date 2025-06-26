# File: translator/urls.py

from modules.views.compress_pdf import CompressPDFView
from modules.views.pdf_to_excel import PDFToExcelView

from django.urls import path

# from modules.views.word_to_pdf import WordAndPPTToPDFView
from modules.views.compress_pdf import CompressPDFView
from modules.views.lock_unlock_pdf import LockUnlockPDFView
from modules.views.protect_pdf import ProtectPDFView
from modules.views.organize_pdf import OrganizePDFView
from modules.views.pagenumber_pdf import AddPageNumberView
from modules.views.add_watermark_to_pdf import AddWatermarkToPDF
from modules.views.repair_pdf import RepairPDFView
from modules.views.excel_to_pdf import ExcelToPDFView
# from modules.views.image_background_remove import RemoveImageBackground
from modules.views.muiltple_pdf_merge import MergePDFsView
from modules.views.pdf_rotator_tool import PDFRotateView
from modules.views.pdf_to_image import  PDFToImagesView
from modules.views.pdf_to_word import pdf_to_word
from modules.views.translater import TranslationAPIView

from modules.views.split_pdf import SplitPDFView
from modules.views.pagenumber_pdf import AddPageNumberView
from modules.views.pdf_rotator_tool import PDFRotateView


urlpatterns = [
    path('translate/', TranslationAPIView.as_view(), name='translate'),
    # path('image-bg-remover/', RemoveImageBackground.as_view(), name='image-bg-remover'),
    path('pdf-to-word/', pdf_to_word, name='pdf_to_word'),
    path('merge-pdfs/', MergePDFsView.as_view(), name='merge_pdfs'),
    
   path('excel-to-pdf/', ExcelToPDFView.as_view(), name='excel_to_pdf'),

    path('pdf-to-excel/', PDFToExcelView.as_view(), name='pdf_to_excel'),
     path('pdf-to-images/', PDFToImagesView.as_view(), name='pdf_to_images'),
     path('add-watermark/', AddWatermarkToPDF.as_view(), name='add_watermark_pdf'),
     
     path('pdf-to-rotate/', PDFRotateView.as_view(), name='pdf_to_rotate'),
     path('repair-pdf/', RepairPDFView.as_view(), name='repair_pdf'),

     path('split-pdf/', SplitPDFView.as_view(), name='split_pdf'),
     path('pagenumber_pdf/', AddPageNumberView.as_view(), name='pagenumber_pdf'),
     path('organize-pdf/', OrganizePDFView.as_view(), name='organize_pdf'),
     path('lock-unlock-pdf/', LockUnlockPDFView.as_view(), name='lock_unlock_pdf'),
     path('protect-pdf/', ProtectPDFView.as_view(), name='protect_pdf'),
     path('compress-pdf/', CompressPDFView.as_view(), name='compress_pdf'),
    #  path('word-ppt-to-pdf/', WordAndPPTToPDFView.as_view(), name='word_ppt_to_pdf'),

]