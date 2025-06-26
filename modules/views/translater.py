# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from googletrans import Translator

# class TranslationAPIView(APIView):
#     def post(self, request):
#         text = request.data.get("text")
#         source = request.data.get("source_language")
#         target = request.data.get("target_language")

#         if not all([text, source, target]):
#             return Response({"error": "Missing required parameters."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             translator = Translator()
#             translated = translator.translate(text, src=source, dest=target)
#             return Response({"translated_text": translated.text})
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
